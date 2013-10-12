from datetime import date
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from braces.views import (
    LoginRequiredMixin,
    StaffuserRequiredMixin,
)
from sendfile import sendfile

from .forms import (
    InvoiceBlankForm,
    InvoiceDraftCreateForm,
    InvoiceLineForm,
    InvoiceUpdateForm,
    TimeRecordForm,
)
from .models import (
    Invoice,
    InvoiceLine,
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
    """https://github.com/johnsensible/django-sendfile"""
    invoice = get_object_or_404(Invoice, pk=pk)
    check_perm(request.user, invoice.contact)
    return sendfile(
        request,
        invoice.pdf.path,
        attachment=True,
        attachment_filename='{}.pdf'.format(invoice.invoice_number)
    )


class ContactInvoiceListView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, ListView):

    template_name = 'invoice/contact_invoice_list.html'

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        self._check_perm(contact)
        return contact

    def get_context_data(self, **kwargs):
        context = super(
            ContactInvoiceListView, self
        ).get_context_data(**kwargs)
        context.update(dict(
            contact=self._get_contact(),
        ))
        return context

    def get_queryset(self):
        contact = self._get_contact()
        return Invoice.objects.filter(contact=contact)


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
        return TimeRecord.objects.filter(
            ticket__contact=contact
        ).order_by(
            'date_started',
            'start_time',
        )


class InvoiceCreateViewMixin(BaseMixin, CreateView):

    model = Invoice

    def _get_contact(self):
        slug = self.kwargs.get('slug')
        contact = get_object_or_404(Contact, slug=slug)
        return contact

    def _check_invoice_settings(self, contact):
        warnings = InvoiceCreate().is_valid(contact)
        for message in warnings:
            messages.warning(self.request, message)

    def get_context_data(self, **kwargs):
        context = super(
            InvoiceCreateViewMixin, self
        ).get_context_data(**kwargs)
        contact = self._get_contact()
        self._check_invoice_settings(contact)
        context.update(dict(
            contact=contact,
        ))
        return context


class InvoiceDetailView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, DetailView):

    model = Invoice


class InvoiceDraftCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, InvoiceCreateViewMixin):

    form_class = InvoiceDraftCreateForm
    template_name = 'invoice/invoice_create_draft_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contact = self._get_contact()
        self.object.user = self.request.user
        return super(InvoiceDraftCreateView, self).form_valid(form)


class InvoiceLineCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, CreateView):

    form_class = InvoiceLineForm
    model = InvoiceLine
    template_name = 'invoice/invoiceline_create_form.html'

    def _get_invoice(self):
        pk = self.kwargs.get('pk')
        invoice = get_object_or_404(Invoice, pk=pk)
        return invoice

    def get_context_data(self, **kwargs):
        context = super(InvoiceLineCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            invoice=self._get_invoice(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.invoice = self._get_invoice()
        self.object.line_number = self.object.invoice.get_next_line_number()
        self.object.user = self.request.user
        return super(InvoiceLineCreateView, self).form_valid(form)


class InvoiceLineUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = InvoiceLineForm
    model = InvoiceLine
    template_name = 'invoice/invoiceline_update_form.html'


class InvoicePdfUpdateView(
        LoginRequiredMixin, CheckPermMixin, BaseMixin, UpdateView):

    form_class = InvoiceBlankForm
    model = Invoice
    template_name = 'invoice/invoice_create_pdf_form.html'

    def _check_invoice_print(self, invoice):
        warnings = InvoicePrint().is_valid(invoice)
        for message in warnings:
            messages.warning(self.request, message)

    def get_object(self, *args, **kwargs):
        obj = super(InvoicePdfUpdateView, self).get_object(*args, **kwargs)
        self._check_invoice_print(obj)
        return obj

    def form_valid(self, form):
        InvoicePrint().create_pdf(self.object, header_image=None)
        messages.info(
            self.request,
            "Created PDF for invoice {}, {} at {} today.".format(
                self.object.invoice_number,
                self.object.contact.name,
                self.object.created.strftime("%H:%M"),
            )
        )
        return HttpResponseRedirect(reverse('invoice.list'))


class InvoiceTimeCreateView(
        LoginRequiredMixin, StaffuserRequiredMixin, InvoiceCreateViewMixin):

    form_class = InvoiceBlankForm
    template_name = 'invoice/invoice_create_time_form.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceTimeCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            timerecords=InvoiceCreate().draft(
                self._get_contact(), datetime.today()
            ),
        ))
        return context

    def form_valid(self, form):
        invoice_create = InvoiceCreate()
        self.object = invoice_create.create(
            self.request.user,
            self._get_contact(),
            datetime.today(),
        )
        #InvoicePrint().create_pdf(self.object, header_image=None)
        messages.info(
            self.request,
            "Draft invoice {} for {} created at {} today.".format(
                self.object.invoice_number,
                self.object.contact.name,
                self.object.created.strftime("%H:%M"),
            )
        )
        return HttpResponseRedirect(reverse('invoice.list'))


class InvoiceListView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, ListView):

    model = Invoice


class InvoiceUpdateView(
        LoginRequiredMixin, StaffuserRequiredMixin, BaseMixin, UpdateView):

    form_class = InvoiceUpdateForm
    model = Invoice
    template_name = 'invoice/invoice_update_form.html'


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

    def get_initial(self):
        return dict(
            date_started=date.today(),
            start_time=datetime.today().time(),
        )

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
        return TimeRecord.objects.filter(
            ticket=ticket
        ).order_by(
            'date_started',
            'start_time',
        )


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
