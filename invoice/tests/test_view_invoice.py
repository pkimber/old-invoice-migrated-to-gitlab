# -*- encoding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse

from crm.tests.factories import ContactFactory
from login.tests.factories import (
    TEST_PASSWORD,
    UserFactory,
)
from .factories import InvoiceSettingsFactory

class TestViewInvoice(TestCase):

    def setUp(self):
      user = UserFactory(username='staff', is_staff=True)
      self.assertTrue(
          self.client.login(username=user.username, password=TEST_PASSWORD)
      )

    def test_post(self):
        InvoiceSettingsFactory()
        contact = ContactFactory()
        url = reverse('invoice.create.draft', kwargs={'slug': contact.slug})
        response = self.client.post(url)
        assert 200 == response.status_code
