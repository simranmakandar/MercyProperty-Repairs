from django.forms import ModelForm, DateInput
from workorder.models import WorkOrderItem, WorkOrder


class DateInput(DateInput):
    input_type = 'date'


class WorkOrderForm(ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['workorder_name', 'property', 'apartment', 'short_desc', 'skill_set',
                  'severity', 'status', 'promised_date', 'completed_date',
                  'estimated_cost', 'actual_cost', 'work_order_date', 'user']
        widgets = {
            'promised_date': DateInput(),
            'completed_date': DateInput(),
            'work_order_date': DateInput(),
        }


class ItemForm(ModelForm):
    class Meta:
        model = WorkOrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        work_order_id = kwargs.pop('work_id')
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['work_order'].initial = work_order_id
