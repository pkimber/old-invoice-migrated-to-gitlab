# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal
from django.core.urlresolvers import reverse
from django.utils import timezone

from contact.tests.factories import ContactFactory
from invoice.models import Invoice, InvoiceLine
from finance.tests.factories import VatCode, VatSettingsFactory
from login.tests.factories import TEST_PASSWORD, UserFactory
from stock.tests.factories import ProductFactory
from .factories import (
    InvoiceContactFactory,
    InvoiceFactory,
    InvoiceSettingsFactory,
)


@pytest.mark.django_db
def test_invoice_create_draft(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    assert 0 == Invoice.objects.count()
    url = reverse('invoice.create.draft', kwargs={'pk': contact.pk})
    data = {
        'invoice_date': timezone.now().date(),
    }
    response = client.post(url, data)
    assert 302 == response.status_code, response.context['form'].errors
    assert 1 == Invoice.objects.count()
    invoice = Invoice.objects.first()
    assert invoice.number == 1
    assert invoice.invoice_number == '000001'


@pytest.mark.django_db
def test_invoice_line_create(client):
    user = UserFactory(username='staff', is_staff=True)
    assert client.login(username=user.username, password=TEST_PASSWORD) is True
    InvoiceSettingsFactory()
    VatSettingsFactory()
    invoice = InvoiceFactory()
    assert 0 == InvoiceLine.objects.count()
    url = reverse('invoice.line.create', args=[invoice.pk])
    data = {
        'product': ProductFactory().pk,
        'description': 'Apple',
        'price': Decimal('3'),
        'quantity': Decimal('1'),
        'units': 'Each',
        'vat_code': VatCode.objects.get(slug=VatCode.STANDARD).pk,
    }
    response = client.post(url, data)
    assert 302 == response.status_code, response.context['form'].errors
    assert 1 == InvoiceLine.objects.count()
