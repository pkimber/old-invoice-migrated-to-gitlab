# -*- encoding: utf-8 -*-
"""
Test time records.
"""
import pytest


from django.test import TestCase

from invoice.models import TimeRecord
from invoice.tests.factories import (
    InvoiceLineFactory,
    ContactFactory,
    TicketFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory
from search.tests.helper import check_search_methods


@pytest.mark.django_db
def test_search_methods():
    time_record = TimeRecordFactory()
    check_search_methods(time_record)


@pytest.mark.django_db
def test_str():
    time_record = TimeRecordFactory()
    str(time_record)


@pytest.mark.django_db
def test_user_can_edit():
    time_record = TimeRecordFactory()
    assert time_record.user_can_edit is True


@pytest.mark.django_db
def test_user_can_edit_invoice_line():
    invoice_line = InvoiceLineFactory()
    time_record = TimeRecordFactory(invoice_line=invoice_line)
    assert time_record.user_can_edit is False
