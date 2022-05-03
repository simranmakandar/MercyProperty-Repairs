from django.db import models
from property.models import Apartment, Property
from user.models import ExtUser


# Create your models here.
class WorkOrder(models.Model):

    severity_choices = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('URGENT', 'Urgent'),

    ]
    status_choices = [
        ('OPEN', 'Open'),
        ('DONE', 'Done')
    ]
    workorder_name = models.CharField(max_length=30, blank=False, default='', verbose_name='Work Order Title')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='Property')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, verbose_name='Apartment Number')
    short_desc = models.CharField(max_length=200, blank=False, default='', verbose_name='Work Order Description')
    skill_set = models.CharField(max_length=200, blank=False, default='', verbose_name='Skillset Required')
    severity = models.CharField(max_length=9, blank=False, default='Low', choices=severity_choices, verbose_name='Severity Level')
    status = models.CharField(max_length=25, blank=False, default='Open', choices=status_choices, verbose_name='Current Status')
    promised_date = models.DateTimeField(blank=True, null=True, verbose_name = 'Promised Completion Date')
    completed_date = models.DateTimeField(blank=True, null=True, verbose_name = 'Actual Completion Date')
    estimated_cost = models.DecimalField(max_digits=8, decimal_places=2, default='0.0', verbose_name = 'Estimated Cost')
    actual_cost = models.DecimalField(max_digits=8, decimal_places=2, default='0.0', verbose_name = 'Actual Cost')
    work_order_date = models.DateTimeField(blank=False, auto_now_add=False, verbose_name = 'Work Order Submitted Date')
    user = models.ForeignKey(ExtUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Assigned Employee')

    def __str__(self):
        return self.workorder_name

class WorkOrderItem(models.Model):
    item_name = models.CharField(max_length=30, blank=False, verbose_name='Item Name')
    item_cost = models.DecimalField(max_digits=8, decimal_places=2, default='0.0', verbose_name='Cost')
    item_quantity = models.IntegerField(default=1, blank=False, verbose_name='Quantity')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name='Associated Work Order')

    def __str__(self):
        return self.item_name
