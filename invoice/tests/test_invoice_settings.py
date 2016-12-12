# -*- encoding: utf-8 -*-
import pytest

from invoice.tests.factories import InvoiceSettingsFactory
from stock.tests.factories import ProductFactory


@pytest.mark.django_db
def test_str():
    obj = InvoiceSettingsFactory(
        name_and_address='Honeydown',
        phone_number='01837',
        time_record_product=None,
    )
    assert 'Honeydown, Phone: 01837' == str(obj)


@pytest.mark.django_db
def test_str_with_time_record_product():
    obj = InvoiceSettingsFactory(
        name_and_address='Honeydown',
        phone_number='01837',
        time_record_product=ProductFactory(name='Apple'),
    )
    assert 'Honeydown, Phone: 01837, Time record: Apple' == str(obj)
