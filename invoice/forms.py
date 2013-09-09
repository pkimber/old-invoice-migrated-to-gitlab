from django import forms

from base.form_utils import (
    RequiredFieldForm,
)
from .models import (
    Invoice,
    TimeRecord,
)


class InvoiceCreateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ()


class TimeRecordForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(TimeRecordForm, self).__init__(*args, **kwargs)
        for name in ('title', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = TimeRecord
        fields = (
            "title",
            "description",
            "date_started",
            "start_time",
            "end_time",
            "billable",
        )
