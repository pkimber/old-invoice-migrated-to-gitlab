# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from finance.tests.factories import VatSettingsFactory
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from .factories import (
    InvoiceContactFactory,
    InvoiceSettingsFactory,
)


class TestViewInvoice(TestCase):

    def setUp(self):
      user = UserFactory(username='staff', is_staff=True)
      self.assertTrue(
          self.client.login(username=user.username, password=TEST_PASSWORD)
      )

    def test_post(self):
        InvoiceSettingsFactory()
        VatSettingsFactory()
        contact = ContactFactory()
        InvoiceContactFactory(contact=contact)
        url = reverse('invoice.create.draft', kwargs={'slug': contact.slug})
        response = self.client.post(url)
        assert 200 == response.status_code
