from datetime import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase

from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
    get_contact_smallholding,
    get_ticket_fence_for_farm,
)
from invoice.tests.scenario import (
    default_scenario_invoice,
    get_invoice_paperwork,
    get_timerecord_fence_dig_holes,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    get_user_web,
    user_contractor,
)


class TestViewPerm(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()
        self.web = get_user_web()
        self.client.login(
            username=self.web.username, password=self.web.username
        )

    def test_contact_invoice_list(self):
        smallholding = get_contact_smallholding()
        url = reverse(
            'invoice.contact.list',
            kwargs={'slug': smallholding.slug}
        )
        self._assert_get_perm_denied(url)

    def test_contact_time_record_list(self):
        farm = get_contact_farm()
        url = reverse(
            'invoice.time.contact.list',
            kwargs={'slug': farm.slug}
        )
        self._assert_get_perm_denied(url)

    def test_invoice_create_draft(self):
        farm = get_contact_farm()
        url = reverse(
            'invoice.create.draft',
            kwargs={'slug': farm.slug}
        )
        self._assert_post_staff_only(url)

    def test_invoice_create_time(self):
        farm = get_contact_farm()
        url = reverse(
            'invoice.create.time',
            kwargs={'slug': farm.slug}
        )
        self._assert_post_staff_only(url)

    def test_invoice_list(self):
        url = reverse('invoice.list')
        self._assert_get_staff_only(url)

    def test_invoice_download(self):
        invoice = InvoiceCreate().create(
            get_user_staff(),
            get_contact_farm(),
            datetime(2013, 12, 31)
        )
        InvoicePrint().create_pdf(invoice, header_image=None)
        url = reverse('invoice.download', kwargs={'pk': invoice.pk})
        self._assert_get_perm_denied(url)

    def test_invoice_detail(self):
        invoice = get_invoice_paperwork()
        url = reverse('invoice.detail', kwargs={'pk': invoice.pk})
        self._assert_get_staff_only(url)

    def test_invoice_line_create(self):
        invoice = get_invoice_paperwork()
        url = reverse('invoice.line.create', kwargs={'pk': invoice.pk})
        self._assert_get_staff_only(url)

    def test_invoice_line_update(self):
        invoice = get_invoice_paperwork()
        url = reverse('invoice.line.update', kwargs={'pk': invoice.pk})
        self._assert_get_staff_only(url)

    def test_invoice_create_pdf(self):
        invoice = get_invoice_paperwork()
        url = reverse('invoice.create.pdf', kwargs={'pk': invoice.pk})
        self._assert_get_staff_only(url)

    def test_invoice_update(self):
        invoice = get_invoice_paperwork()
        url = reverse('invoice.update', kwargs={'pk': invoice.pk})
        self._assert_get_staff_only(url)

    def test_timerecord_list(self):
        url = reverse('invoice.time')
        self._assert_get_staff_only(url)

    def test_timerecord_create(self):
        fence = get_ticket_fence_for_farm()
        url = reverse(
            'invoice.time.create',
            kwargs={'pk': fence.pk}
        )
        self._assert_get_staff_only(url)

    def test_ticket_timerecord_list(self):
        fence = get_ticket_fence_for_farm()
        url = reverse(
            'invoice.time.ticket.list',
            kwargs={'pk': fence.pk}
        )
        self._assert_get_perm_denied(url)

    def test_user_timerecord_list(self):
        fence = get_ticket_fence_for_farm()
        url = reverse('invoice.time.user.list')
        self._assert_get_staff_only(url)

    def test_timerecord_update(self):
        dig = get_timerecord_fence_dig_holes()
        url = reverse(
            'invoice.time.update',
            kwargs={'pk': dig.pk}
        )
        self._assert_get_staff_only(url)

    def _assert_get_perm_denied(self, url):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            403,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.web.username, url
            )
        )

    def _assert_get_staff_only(self, url):
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.web.username, url
            )
        )

    def _assert_post_staff_only(self, url):
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            302,
            "status {}: user '{}' should not have access "
            "to this url: '{}'".format(
                response.status_code, self.web.username, url
            )
        )
