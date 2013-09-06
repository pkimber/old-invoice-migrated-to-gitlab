from django import forms

from .models import TimeRecord


class TimeRecordForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TimeRecordForm, self).__init__(*args, **kwargs)
        for name in ('name', 'description'):
            self.fields[name].widget.attrs.update(
                {'class': 'pure-input-2-3'}
            )

    class Meta:
        model = TimeRecord
        fields = (
            "name",
            "description",
            "date_started",
            "start_time",
            "end_time",
            "billable",
        )
