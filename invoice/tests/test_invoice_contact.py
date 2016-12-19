# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal
from django.core.urlresolvers import reverse

from contact.tests.factories import ContactFactory
from invoice.tests.factories import InvoiceContactFactory
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_get_absolute_url():
    contact = ContactFactory(user=UserFactory(username='alan'))
    obj = InvoiceContactFactory(contact=contact)
    expect = reverse('contact.detail', args=[contact.pk])
    assert expect == obj.get_absolute_url()


@pytest.mark.django_db
def test_str():
    user = UserFactory(first_name='Alan', last_name='Jones')
    contact = ContactFactory(user=user)
    obj = InvoiceContactFactory(contact=contact, hourly_rate=Decimal('12.34'))
    assert 'Alan Jones @ 12.34' == str(obj)


@pytest.mark.django_db
def test_str_no_hourly_rate():
    user = UserFactory(first_name='Alan', last_name='Jones')
    contact = ContactFactory(user=user)
    obj = InvoiceContactFactory(contact=contact, hourly_rate=None)
    assert 'Alan Jones' == str(obj)
