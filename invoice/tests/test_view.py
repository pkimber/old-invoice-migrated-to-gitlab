"""Simple tests to make sure a view doesn't throw any exceptions"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from crm.tests.scenario import (
    contact_contractor,
    get_contact_farm,
    get_contact_smallholding,
    get_ticket_fence_for_farm,
)
from invoice.tests.scenario import (
    get_timerecord_fence_dig_holes,
    time_fencing,
    time_paperwork,
    invoice_settings,
)
from login.tests.scenario import (
    get_user_staff,
    user_contractor,
    user_default,
)


class TestView(TestCase):

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
        invoice_settings()
        time_fencing()
        time_paperwork()

    def test_contact_invoice_list(self):
        smallholding = get_contact_smallholding()
        url = reverse(
            'invoice.contact.list',
            kwargs={'slug': smallholding.slug}
        )
        self._assert_get(url)

    def test_contact_time_record_list(self):
        farm = get_contact_farm()
        url = reverse(
            'invoice.time.contact.list',
            kwargs={'slug': farm.slug}
        )
        self._assert_get(url)

    def test_invoice_create(self):
        farm = get_contact_farm()
        url = reverse(
            'invoice.create.time',
            kwargs={'slug': farm.slug}
        )
        self._assert_post(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        self._assert_get(url)

    def test_timerecord_create(self):
        fence = get_ticket_fence_for_farm()
        url = reverse(
            'invoice.time.create',
            kwargs={'pk': fence.pk}
        )
        self._assert_get(url)

    def test_timerecord_list(self):
        url = reverse('invoice.time')
        self._assert_get(url)

    def test_ticket_timerecord_list(self):
        fence = get_ticket_fence_for_farm()
        url = reverse(
            'invoice.time.ticket.list',
            kwargs={'pk': fence.pk}
        )
        self._assert_get(url)

    def test_timerecord_update(self):
        dig = get_timerecord_fence_dig_holes()
        url = reverse(
            'invoice.time.update',
            kwargs={'pk': dig.pk}
        )
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
        staff = get_user_staff()
        self.client.login(
            username=staff.username,
            password=staff.username,
        )
