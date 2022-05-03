from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from workorder.forms import WorkOrderForm, ItemForm
from workorder.models import WorkOrder, WorkOrderItem
from django.db.models import Count
from django.forms import ModelForm, DateInput
from django.core.paginator import Paginator
from django.shortcuts import render
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import csv
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse
from .models import WorkOrder, WorkOrderItem
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def homeView(request):
    return render(request, 'home.html')


class DateInput(DateInput):
    input_type = 'date'


def dashboardView(request):
    open_wo_count = WorkOrder.objects.filter(status='OPEN').count()
    severity_count = WorkOrder.objects.filter(severity='URGENT').count()
    total_wo = WorkOrder.objects.all().count()
    # print(open_wo_count)
    return render(request, 'workorder/dashboard.html', {'open_wo_count': open_wo_count,
                                                        'severity_count': severity_count,
                                                        'total_wo': total_wo})
    # return render(request, 'workorder/dashboard.html')


class WorkOrderList(LoginRequiredMixin, ListView):
    template_name = "workorder_list.html"
    model = WorkOrder
    context_object_name = 'orders'
    paginate_by = 4
    queryset = WorkOrder.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super(WorkOrderList, self).get_context_data(**kwargs)
    #     context["orders"] = WorkOrder.objects.all()
    #     return context


class WorkOrderList1(LoginRequiredMixin, ListView):
    template_name = "workorder_list.html"
    model = WorkOrder

    def get_context_data(self, **kwargs):
        context = super(WorkOrderList1, self).get_context_data(**kwargs)
        context["orders"] = WorkOrder.objects.filter(property__user=self.request.user)
        return context


class WorkOrderList2(LoginRequiredMixin, ListView):
    template_name = "workorder_list.html"
    model = WorkOrder

    def get_context_data(self, **kwargs):
        context = super(WorkOrderList2, self).get_context_data(**kwargs)
        context["orders"] = WorkOrder.objects.filter(user__is_worker=True)
        return context


class CreateWorkOrder(LoginRequiredMixin, CreateView):
    template_name = "workorder/create_workorder.html"
    model = WorkOrder
    form_class = WorkOrderForm
    success_url = reverse_lazy("workorder_list")


class UpdateWorkOrder(LoginRequiredMixin, UpdateView):
    template_name = "workorder/update_workorder.html"
    model = WorkOrder
    form_class = WorkOrderForm
    success_url = reverse_lazy("workorder_list")


class WorkOrderDetail(LoginRequiredMixin, DetailView):
    template_name = "workorder/workorder_detail.html"
    model = WorkOrder

    def get_context_data(self, **kwargs):
        context = super(WorkOrderDetail, self).get_context_data(**kwargs)
        context["items"] = WorkOrderItem.objects.filter(work_order=self.object)
        return context


class DeleteWorkOrder(LoginRequiredMixin, DeleteView):
    template_name = "workorder/delete_workorder.html"
    model = WorkOrder
    fields = "__all__"
    success_url = reverse_lazy("workorder_list")


class CreateWorkOrderItems(LoginRequiredMixin, CreateView):
    template_name = "workorder/items/create.html"
    model = WorkOrderItem
    form_class = ItemForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request, 'work_id': self.kwargs['work_order_id']})
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('order_detail', kwargs={'pk': self.kwargs['work_order_id']})


class UpdateWorkOrderItems(LoginRequiredMixin, UpdateView):
    template_name = "workorder/items/update.html"
    model = WorkOrderItem
    fields = ('item_name', 'item_cost', 'item_quantity')
    success_url = reverse_lazy("home")

    def get_success_url(self, **kwargs):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.work_order_id})


class DeleteWorkOrderItems(LoginRequiredMixin, DeleteView):
    template_name = "workorder/items/delete.html"
    model = WorkOrderItem
    fields = "__all__"

    def get_success_url(self, **kwargs):
        return reverse_lazy('order_detail', kwargs={'pk': self.object.work_order.id})


class ExportFilterForms(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ('status', 'user', 'property')


@staff_member_required
def export_filter_work(request):
    template_name = "workorder/workorderfilter.html"
    form_class = ExportFilterForms()
    return render(request, template_name, {'form': form_class})


@staff_member_required
def export_work_orders(request):
    form = ExportFilterForms(request.POST)
    response = HttpResponse(content_type='text/csv')
    if form.is_valid():
        cs_value = form.cleaned_data['status']
        assigned_user = form.cleaned_data['user']
        assigned_apartment = form.cleaned_data['property']

    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'Apartment Number', 'Description', 'Skill Set Required'
                        , 'Severity Level', 'Current Status', 'Desired Completion Date', 'Estimated Cost'
                        , 'Assigned Employee', 'Actual Completion Date', 'Actual Cost'])
    if assigned_user and assigned_apartment is None:
        wo_object = WorkOrder.objects.filter(status=cs_value)
    elif assigned_apartment is None:
        wo_object = WorkOrder.objects.filter(status=cs_value, user=assigned_user)
    elif assigned_user is None:
        wo_object = WorkOrder.objects.filter(status=cs_value, property=assigned_apartment)
    else:
        wo_object = WorkOrder.objects.filter(status=cs_value, user=assigned_user, property=assigned_apartment)

    for wo in wo_object.values_list('id', 'workorder_name', 'apartment__apt_num', 'short_desc', 'skill_set', 'severity',
                                    'status', 'promised_date', 'estimated_cost', 'user__username', 'completed_date',
                                    'actual_cost'):
        writer.writerow(wo)

    response['Content-Disposition'] = 'attachment; filename="workorders.csv"'

    return response


@staff_member_required
def export_PDFfilter_work(request):
    template_name = "workorder/workorderPDFfilter.html"
    form_class = ExportFilterForms()
    return render(request, template_name, {'form': form_class})


@staff_member_required
def export_PDFwork_orders(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)

    form = ExportFilterForms(request.POST)

    if form.is_valid():
        cs_value = form.cleaned_data['status']
        assigned_user = form.cleaned_data['user']
        assigned_apartment = form.cleaned_data['property']

    lines = []

    if assigned_user and assigned_apartment is None:
        wo_object = WorkOrder.objects.filter(status=cs_value)
    elif assigned_apartment is None:
        wo_object = WorkOrder.objects.filter(status=cs_value, user=assigned_user)
    elif assigned_user is None:
        wo_object = WorkOrder.objects.filter(status=cs_value, property=assigned_apartment)
    else:
        wo_object = WorkOrder.objects.filter(status=cs_value, user=assigned_user, property=assigned_apartment)

    lines.append("Here is your generated Report!")
    for order in wo_object:
        # print(order.customer_name)
        lines.append(" ")
        lines.append("Work Order Name: " + "       " + str(order.workorder_name))
        lines.append("Property: " + "              " + str(order.property))
        lines.append("Apartment: " + "             " + str(order.apartment))
        lines.append("Short Description: " + "     " + str(order.short_desc))
        lines.append("Skill Set: " + "             " + str(order.skill_set))
        lines.append("Severity: " + "              " + str(order.severity))
        lines.append("Status: " + "                " + str(order.status))
        lines.append("Promised Date: " + "         " + str(order.promised_date))
        lines.append("Completed Date: " + "        " + str(order.completed_date))
        lines.append("Estimated Cost: " + "        " + str(order.estimated_cost))
        lines.append("Actual Cost: " + "           " + str(order.actual_cost))
        lines.append("Work Order Date: " + "       " + str(order.work_order_date))

    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='workorders.pdf')


@login_required
def view_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica", 14)

    # orders = WorkOrder.objects.filter(workorder_name=request.user.id)

    orders = WorkOrder.objects.all()

    lines = []

    lines.append("Here is your generated Report!")
    for order in orders:
        # print(order.customer_name)
        lines.append(" ")
        lines.append("Work Order Name: " + "       " + str(order.workorder_name))
        lines.append("Property: " + "              " + str(order.property))
        lines.append("Apartment: " + "             " + str(order.apartment))
        lines.append("Short Description: " + "     " + str(order.short_desc))
        lines.append("Skill Set: " + "             " + str(order.skill_set))
        lines.append("Severity: " + "              " + str(order.severity))
        lines.append("Status: " + "                " + str(order.status))
        lines.append("Promised Date: " + "         " + str(order.promised_date))
        lines.append("Completed Date: " + "        " + str(order.completed_date))
        lines.append("Estimated Cost: " + "        " + str(order.estimated_cost))
        lines.append("Actual Cost: " + "           " + str(order.actual_cost))
        lines.append("Work Order Date: " + "       " + str(order.work_order_date))
        lines.append(" ")

    for line in lines:
        textobj.textLine(line)

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')
