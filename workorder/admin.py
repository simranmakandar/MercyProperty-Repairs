from django.contrib import admin
from .models import WorkOrder, WorkOrderItem


class WorkOrderItemInline(admin.TabularInline):
    model = WorkOrderItem


class WorkOrderAdmin(admin.ModelAdmin):
    model = WorkOrder
    list_display = ['workorder_name', 'property', 'apartment', 'short_desc', 'skill_set', 'severity', 'status',
                    'promised_date', 'completed_date', 'estimated_cost', 'actual_cost', 'work_order_date', 'user']
    list_filter = ['apartment', 'skill_set', 'severity', 'status', 'promised_date',
                   'work_order_date', 'completed_date', 'user']
    inlines = [WorkOrderItemInline]
    fieldset = (
        ('Work Order', {
            'fields': ('workorder_name', 'property_id', 'apartment_id', 'short_desc', 'skill_set', 'severity',
                       'status', 'promised_date', 'completed_date', 'estimated_cost',
                       'actual_cost', 'work_order_date', 'user_id')
        })
    )
    add_fieldset = (
        ('Work Order', {
            'fields': ('workorder_name', 'property_id', 'apartment_id', 'short_desc', 'skill_set', 'severity',
                       'status', 'promised_date', 'completed_date', 'estimated_cost',
                       'actual_cost', 'work_order_date', 'user_id')
        })
    )

admin.site.register(WorkOrder, WorkOrderAdmin)

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;' \
                                      'filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'