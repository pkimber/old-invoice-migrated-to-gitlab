# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django import forms

from base.form_utils import (
    RequiredFieldForm,
)
from .models import (
    Invoice,
    InvoiceLine,
    TimeRecord,
)


class InvoiceDraftCreateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            'invoice_date',
        )


class InvoiceBlankForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = ()


class InvoiceBlankTodayForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super(InvoiceBlankTodayForm, self).__init__(*args, **kwargs)
        iteration_end = self.fields['iteration_end']
        iteration_end.initial = date.today()


    class Meta:
        model = Invoice
        fields = ()

    iteration_end = forms.DateField()


class InvoiceLineForm(forms.ModelForm):

    class Meta:
        model = InvoiceLine
        fields = (
            'description',
            'quantity',
            'units',
            'price',
            'vat_rate',
        )


class InvoiceUpdateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            'invoice_date',
        )


class TimeRecordForm(RequiredFieldForm):

    paginate_by = 20

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
