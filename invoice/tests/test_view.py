"""Simple tests to make sure a view doesn't throw any exceptions"""
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
    make_user_contact,
)
from invoice.tests.model_maker import (
    make_invoice_settings,
    make_time_record,
)
from login.tests.model_maker import make_user


class TestView(TestCase):

    def setUp(self):
        """tom has access to contact icl"""
        self.tom = make_user('tom', is_staff=True)
        self.icl = make_contact('icl', 'ICL', hourly_rate=Decimal('20.00'))
        make_user_contact(self.tom, self.icl)
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
        self._assert_get(url)

    def test_invoice_create(self):
        url = reverse(
            'invoice.create',
            kwargs={'slug': self.icl.slug}
        )
        self._assert_post(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        self._assert_get(url)

    def test_timerecord_create(self):
        url = reverse('invoice.time.create', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def test_timerecord_list(self):
        url = reverse('invoice.time')
        self._assert_get(url)

    def test_ticket_timerecord_list(self):
        url = reverse('invoice.time.ticket.list', kwargs={'pk': self.sew.pk})
        self._assert_get(url)

    def test_timerecord_update(self):
        url = reverse('invoice.time.update', kwargs={'pk': self.pillow.pk})
        self._assert_get(url)

    def _assert_get(self, url):
        # User must be logged in to access this URL
        response = self.client.get(url)
        self._assert_access_denied(url, response)
        self._login_user()
        response = self.client.get(url)
        self._assert_access(url, response)

    def _assert_post(self, url):
        # User must be logged in to access this URL
        response = self.client.post(url)
        self._assert_access_denied(url, response)
        self._login_user()
        response = self.client.post(url)
        self._assert_redirect(url, response)

    def _assert_access(self, url, response):
        self.assertEqual(
            response.status_code,
            200,
            'status {}\n{}'.format(response.status_code, response),
        )

    def _assert_access_denied(self, url, response):
        self.assertEqual(
            response.status_code,
            302,
            'status {}\n{}'.format(response.status_code, response),
        )

    def _assert_redirect(self, url, response):
        self.assertEqual(
            response.status_code,
            302,
            'status {}\n{}'.format(response.status_code, response),
        )

    def _login_user(self):
        """Log the user in so they can access this URL"""
        self.client.login(
            username=self.tom.username,
            password=self.tom.username,
        )
