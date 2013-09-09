from datetime import datetime
from datetime import time
from decimal import Decimal

from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.model_maker import (
    make_contact,
    make_note,
    make_priority,
    make_ticket,
)
from invoice.service import (
    InvoicePrint,
)
from invoice.tests.model_maker import (
    make_invoice,
    make_invoice_line,
    make_invoice_settings,
    make_time_record,
)
from login.tests.model_maker import make_user


class TestViewPerm(TestCase):

    def setUp(self):
        self.sam = make_user('sam', is_staff=True)
        self.tom = make_user('tom')
        self.client.login(
            username=self.tom.username, password=self.tom.username
        )
        self.icl = make_contact('icl', 'ICL', hourly_rate=Decimal('20.00'))
        self.sew = make_ticket(
            self.icl, self.tom, 'Sew', make_priority('Low', 1)
        )
        self.note = make_note(
            self.sew, self.tom, 'Cut out some material and make a pillow case'
        )
        self.pillow = make_time_record(
            self.sew,
            self.tom,
            'Make a pillow case',
            datetime(2012, 9, 1),
            time(9, 0),
            time(12, 30),
            True,
        )
        make_invoice_settings(
            vat_rate=Decimal('0.20'),
            vat_number='',
            name_and_address='Patrick Kimber, Hatherleigh, EX20 1AB',
            phone_number='01234 234 456',
            footer="Please pay by bank transfer<br />Thank you"
        )

    def test_contact_time_record_list(self):
        url = reverse(
            'invoice.time.contact.list',
            kwargs={'slug': self.icl.slug}
        )
        self._assert_get_perm_denied(url)

    def test_invoice_create(self):
        url = reverse(
            'invoice.create',
            kwargs={'slug': self.icl.slug}
        )
        self._assert_post_staff_only(url)

    def test_invoice_download(self):
        invoice = make_invoice(
            invoice_date=datetime.today(),
            contact=self.icl,
        )
        make_invoice_line(invoice, 1, 1.3, 'hours', 300.00, 0.20)
        make_invoice_line(invoice, 2, 2.4, 'hours', 200.23, 0.20)
        InvoicePrint().create_pdf(invoice, header_image=None)
        url = reverse('invoice.download', kwargs={'pk': invoice.pk})
        self._assert_get_perm_denied(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        self._assert_get_staff_only(url)

    def test_timerecord_create(self):
        url = reverse('invoice.time.create', kwargs={'pk': self.sew.pk})
        self._assert_get_staff_only(url)

    def test_timerecord_list(self):
        url = reverse('invoice.time')
        self._assert_get_staff_only(url)

    def test_ticket_timerecord_list(self):
        url = reverse('invoice.time.ticket.list', kwargs={'pk': self.sew.pk})
        self._assert_get_perm_denied(url)

    def test_timerecord_update(self):
        url = reverse('invoice.time.update', kwargs={'pk': self.pillow.pk})
        self._assert_get_staff_only(url)

    def _assert_get_perm_denied(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )

    def _assert_get_staff_only(self, url):
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )

    def _assert_post_staff_only(self, url):
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.tom.username, url
            )
        )
