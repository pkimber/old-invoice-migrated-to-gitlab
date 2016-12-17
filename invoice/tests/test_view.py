# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal
from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from invoice.models import InvoiceContact
from invoice.tests.factories import InvoiceContactFactory
from login.tests.factories import TEST_PASSWORD, UserFactory


@pytest.mark.django_db
def test_invoice_contact_create(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    url = reverse(
        'invoice.contact.create',
        kwargs={'slug': contact.user.username}
    )
    data = {
        'hourly_rate': Decimal('12.34'),
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.user.username])
    assert expect == response['Location']
    invoice_contact = InvoiceContact.objects.get(contact=contact)
    assert Decimal('12.34') == invoice_contact.hourly_rate


@pytest.mark.django_db
def test_invoice_contact_update(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    url = reverse(
        'invoice.contact.update',
        kwargs={'slug': contact.user.username}
    )
    data = {
        'hourly_rate': Decimal('12.34'),
    }
    response = client.post(url, data)
    assert 302 == response.status_code
    expect = reverse('contact.detail', args=[contact.user.username])
    assert expect == response['Location']
    invoice_contact = InvoiceContact.objects.get(contact=contact)
    assert Decimal('12.34') == invoice_contact.hourly_rate
