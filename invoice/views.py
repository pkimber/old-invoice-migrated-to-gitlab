from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)
from sendfile import sendfile

from .forms import (
    InvoiceCreateForm,
    TimeRecordForm,
)
from .models import (
    Invoice,
    TimeRecord,
)
from base.view_utils import BaseMixin
from crm.models import (
    Contact,
    Ticket,
)
from crm.views import (
    check_perm,
    CheckPermMixin,
)
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)


@login_required
def invoice_download(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    check_perm(request.user, invoice.contact)
    return sendfile(request, invoice.pdf.path)


class ContactTimeRecordListView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, ListView):

    template_name = 'invoice/contact_timerecord_list.html'

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        self._check_perm(contact)
        return contact

    def get_context_data(self, **kwargs):
        context = super(
            ContactTimeRecordListView, self
        ).get_context_data(**kwargs)
        context.update(dict(
            contact=self._get_contact(),
        ))
        return context

    def get_queryset(self):
        contact = self._get_contact()
        return TimeRecord.objects.filter(ticket__contact=contact)


class InvoiceCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = InvoiceCreateForm
    model = Invoice

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        return contact

    def get_context_data(self, **kwargs):
        context = super(InvoiceCreateView, self).get_context_data(**kwargs)
        contact = self._get_contact()
        invoice_create = InvoiceCreate(datetime.today())
        warnings = invoice_create.is_valid(contact)
        for message in warnings:
            messages.warning(self.request, message)
        context.update(dict(
            contact=self._get_contact(),
            timerecords=invoice_create.draft(contact),
        ))
        return context

    def form_valid(self, form):
        invoice_create = InvoiceCreate(datetime.today())
        self.object = invoice_create.create(self._get_contact())
        InvoicePrint().create_pdf(self.object, header_image=None)
        messages.info(
            self.request,
            "Invoice {} for {} created at {} today.".format(
                self.object.invoice_number,
                self.object.contact.name,
                self.object.date_created.strftime("%H:%M"),
            )
        )
        return HttpResponseRedirect(reverse('invoice.list'))


class InvoiceListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Invoice


class TimeRecordCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = TimeRecordForm
    model = TimeRecord

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=pk)
        return ticket

    def get_context_data(self, **kwargs):
        context = super(TimeRecordCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = self._get_ticket()
        self.object.user = self.request.user
        return super(TimeRecordCreateView, self).form_valid(form)


class TimeRecordListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):
    model = TimeRecord


class TicketTimeRecordListView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, ListView):

    template_name = 'invoice/ticket_timerecord_list.html'

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=pk)
        self._check_perm(ticket.contact)
        return ticket

    def get_context_data(self, **kwargs):
        context = super(
            TicketTimeRecordListView, self
        ).get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def get_queryset(self):
        ticket = self._get_ticket()
        return TimeRecord.objects.filter(ticket=ticket)


class TimeRecordUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = TimeRecordForm
    model = TimeRecord

    def get_context_data(self, **kwargs):
        context = super(TimeRecordUpdateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self.object.ticket,
        ))
        return context
