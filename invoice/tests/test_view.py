# -*- encoding: utf-8 -*-
"""Simple tests to make sure a view doesn't throw any exceptions"""
from datetime import date

from django.core.urlresolvers import reverse
from django.test import TestCase

from base.tests.test_utils import PermTestCase
from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
    get_contact_smallholding,
    get_ticket_fence_for_farm,
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
#from login.tests.factories import TEST_PASSWORD
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


class TestView(PermTestCase):

    def setUp(self):
        self.setup_users()

    #def setUp(self):
    #    user_contractor()
    #    default_scenario_login()
    #    default_scenario_crm()
    #    default_scenario_invoice()

    def test_contact_invoice_list(self):
        #smallholding = get_contact_smallholding()
        contact = ContactFactory()
        url = reverse(
            'invoice.contact.list',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_contact_time_record_list(self):
        #farm = get_contact_farm()
        contact = ContactFactory()
        url = reverse(
            'invoice.time.contact.list',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_create_draft(self):
        #farm = get_contact_farm()
        InvoiceSettingsFactory()
        contact = ContactFactory()
        url = reverse(
            'invoice.create.draft',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_create_time(self):
        #farm = get_contact_farm()
        InvoiceSettingsFactory()
        contact = ContactFactory()
        url = reverse(
            'invoice.create.time',
            kwargs={'slug': contact.slug}
        )
        self._assert_staff(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        #self._assert_get(url)
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
        #invoice = get_invoice_paperwork()
        invoice = InvoiceFactory()
        url = reverse('invoice.detail', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_line_create(self):
        #invoice = get_invoice_paperwork()
        invoice = InvoiceFactory()
        url = reverse('invoice.line.create', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_line_update(self):
        #invoice = get_invoice_paperwork()
        invoice = InvoiceFactory()
        InvoiceLineFactory(invoice=invoice)
        url = reverse('invoice.line.update', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_create_pdf(self):
        #invoice = get_invoice_paperwork()
        invoice = InvoiceFactory()
        url = reverse('invoice.create.pdf', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_invoice_update(self):
        #invoice = get_invoice_paperwork()
        invoice = InvoiceFactory()
        url = reverse('invoice.update', kwargs={'pk': invoice.pk})
        self._assert_staff(url)

    def test_ticket_timerecord_list(self):
        #fence = get_ticket_fence_for_farm()
        ticket = TicketFactory()
        url = reverse(
            'invoice.time.ticket.list',
            kwargs={'pk': ticket.pk}
        )
        self._assert_staff(url)

    def test_timerecord_create(self):
        #fence = get_ticket_fence_for_farm()
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
        #dig = get_timerecord_fence_dig_holes()
        time_record = TimeRecordFactory()
        url = reverse(
            'invoice.time.update',
            kwargs={'pk': time_record.pk}
        )
        self._assert_staff(url)

    #def _assert_get(self, url):
    #    # User must be logged in to access this URL
    #    response = self.client.get(url)
    #    self._assert_access_denied(url, response)
    #    self._login_user()
    #    response = self.client.get(url)
    #    self._assert_access(url, response)

    #def _assert_post(self, url):
    #    # User must be logged in to access this URL
    #    response = self.client.post(url)
    #    self._assert_access_denied(url, response)

    #def _assert_access(self, url, response):
    #    self.assertEqual(
    #        response.status_code,
    #        200,
    #        'status {}\n{}'.format(response.status_code, response),
    #    )

    #def _assert_access_denied(self, url, response):
    #    self.assertEqual(
    #        response.status_code,
    #        302,
    #        'status {}\n{}'.format(response.status_code, response),
    #    )

    #def _login_user(self):
    #    """Log the user in so they can access this URL"""
    #    staff = get_user_staff()
    #    self.client.login(
    #        username=staff.username,
    #        password=TEST_PASSWORD,
    #    )
