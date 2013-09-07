from datetime import datetime

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    View,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)

from .forms import TimeRecordForm
from .models import (
    Invoice,
    TimeRecord,
)
from crm.models import (
    Contact,
    Ticket,
)
from crm.views import CheckPermMixin
from invoice.service import (
    InvoiceCreate,
)


class ContactTimeRecordListView(LoginRequiredMixin, CheckPermMixin, ListView):

    template_name = 'invoice/contact_timerecord_list.html'

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        self._check_perm(contact)
        return contact

    def get_context_data(self, **kwargs):
        context = super(ContactTimeRecordListView, self).get_context_data(**kwargs)
        context.update(dict(
            contact=self._get_contact(),
        ))
        return context

    def get_queryset(self):
        contact = self._get_contact()
        return TimeRecord.objects.filter(ticket__contact=contact)


class InvoiceCreateView(LoginRequiredMixin, StaffuserRequiredMixin, View):

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        return contact

    def post(self, request, *args, **kwargs):
        invoice_create = InvoiceCreate(datetime.today())
        invoice_create.create(self._get_contact())
        return HttpResponseRedirect(reverse('invoice.list'))


class InvoiceListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    model = Invoice


class InvoiceDraftListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):

    template_name = 'invoice/invoice_draft.html'

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        return contact

    def get_context_data(self, **kwargs):
        context = super(InvoiceDraftListView, self).get_context_data(**kwargs)
        context.update(dict(
            contact=self._get_contact(),
        ))
        return context

    def get_queryset(self):
        contact = self._get_contact()
        invoice_create = InvoiceCreate(datetime.today())
        warnings = invoice_create.is_valid(contact)
        for message in warnings:
            messages.warning(self.request, message)
        return invoice_create.draft(contact)


class TimeRecordCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CreateView):

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


class TimeRecordListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    model = TimeRecord


class TicketTimeRecordListView(LoginRequiredMixin, CheckPermMixin, ListView):

    template_name = 'invoice/ticket_timerecord_list.html'

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=pk)
        self._check_perm(ticket.contact)
        return ticket

    def get_context_data(self, **kwargs):
        context = super(TicketTimeRecordListView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def get_queryset(self):
        ticket = self._get_ticket()
        return TimeRecord.objects.filter(ticket=ticket)


class TimeRecordUpdateView(LoginRequiredMixin, StaffuserRequiredMixin, UpdateView):

    form_class = TimeRecordForm
    model = TimeRecord

    def get_context_data(self, **kwargs):
        context = super(TimeRecordUpdateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self.object.ticket,
        ))
        return context
