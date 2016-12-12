# -*- encoding: utf-8 -*-
from datetime import date

from django import forms

from base.form_utils import (
    RequiredFieldForm,
)
from .models import (
    Invoice,
    InvoiceContact,
    InvoiceLine,
    QuickTimeRecord,
    TimeRecord,
)


class InvoiceContactForm(forms.ModelForm):

    class Meta:
        model = InvoiceContact
        fields = (
            'hourly_rate',
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
            'product',
            'description',
            'quantity',
            'units',
            'price',
            'vat_code',
        )


class InvoiceUpdateForm(forms.ModelForm):

    class Meta:
        model = Invoice
        fields = (
            'invoice_date',
        )


class QuickTimeRecordEmptyForm(forms.ModelForm):

    class Meta:
        model = QuickTimeRecord
        fields = ()


class QuickTimeRecordForm(RequiredFieldForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('description',):
            self.fields[name].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = QuickTimeRecord
        fields = (
            'description',
            'time_code',
            'chargeable',
        )


class TimeRecordForm(RequiredFieldForm):

    paginate_by = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'pure-input-2-3'})

    class Meta:
        model = TimeRecord
        fields = (
            "title",
            "time_code",
            "date_started",
            "start_time",
            "end_time",
            "billable",
        )
