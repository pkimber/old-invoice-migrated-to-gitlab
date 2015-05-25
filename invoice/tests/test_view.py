# -*- encoding: utf-8 -*-
"""Simple tests to make sure a view doesn't throw any exceptions"""
from datetime import date

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase
from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


class TestView(PermTestCase):

    def setUp(self):
        self.setup_users()

    def test_contact_invoice_list(self):
        contact = ContactFactory()
        url = reverse(
            'invoice.contact.list',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_contact_time_record_list(self):
        contact = ContactFactory()
        url = reverse(
            'invoice.time.contact.list',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_create_draft(self):
        InvoiceSettingsFactory()
        contact = ContactFactory()
        url = reverse(
            'invoice.create.draft',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_create_time(self):
        InvoiceSettingsFactory()
        contact = ContactFactory()
        url = reverse(
            'invoice.create.time',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        self._assert_staff(url)

    def test_invoice_download(self):
        InvoiceSettingsFactory()
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2013, 12, 1))
        TimeRecordFactory(ticket=ticket)
        invoice = InvoiceCreate().create(
            UserFactory(),
            contact,
            date(2013, 12, 31)
        )
        InvoicePrint().create_pdf(invoice, header_image=None)
        url = reverse('invoice.download', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_detail(self):
        invoice = InvoiceFactory()
        url = reverse('invoice.detail', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_line_create(self):
        invoice = InvoiceFactory()
        url = reverse('invoice.line.create', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_line_update(self):
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice)
        url = reverse('invoice.line.update', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_create_pdf(self):
        invoice = InvoiceFactory()
        url = reverse('invoice.create.pdf', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_update(self):
        invoice = InvoiceFactory()
        url = reverse('invoice.update', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_ticket_timerecord_list(self):
        ticket = TicketFactory()
        url = reverse(
            'invoice.time.ticket.list',
            kwargs={'pk': ticket.pk}
        )
        self._assert_staff(url)

    def test_timerecord_create(self):
        ticket = TicketFactory()
        url = reverse(
            'invoice.time.create',
            kwargs={'pk': ticket.pk}
        )
        self._assert_staff(url)

    def test_timerecord_list(self):
        url = reverse('invoice.time')
        self._assert_staff(url)

    def test_timerecord_update(self):
        time_record = TimeRecordFactory()
        url = reverse(
            'invoice.time.update',
            kwargs={'pk': time_record.pk}
        )
        self._assert_staff(url)
