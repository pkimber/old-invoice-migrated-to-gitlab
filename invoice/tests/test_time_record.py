# -*- encoding: utf-8 -*-
"""
Test time records.
"""
import pytest

from crm.tests.factories import TicketFactory
from invoice.models import (
    InvoiceError,
    TimeRecord,
)
from invoice.tests.factories import (
    InvoiceLineFactory,
    TimeRecordCategoryFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory
from search.tests.helper import check_search_methods


@pytest.mark.django_db
def test_search_methods():
    time_record = TimeRecordFactory()
    check_search_methods(time_record)


@pytest.mark.django_db
def test_start():
    user = UserFactory()
    category = TimeRecordCategoryFactory()
    ticket = TicketFactory()
    time_record = TimeRecord.objects.start(ticket, user, category)
    assert category == time_record.category
    assert ticket == time_record.ticket
    assert time_record.end_time is None
    assert time_record.start_time is not None
    assert user == time_record.user


@pytest.mark.django_db
def test_start_and_stop():
    user = UserFactory()
    running = TimeRecordFactory(user=user, end_time=None)
    assert running.end_time is None
    category = TimeRecordCategoryFactory()
    ticket = TicketFactory()
    time_record = TimeRecord.objects.start(ticket, user, category)
    assert category == time_record.category
    assert category.description == time_record.title
    assert time_record.billable is False
    assert time_record.end_time is None
    assert time_record.start_time is not None
    assert user == time_record.user
    running.refresh_from_db()
    assert running.end_time == time_record.start_time


@pytest.mark.django_db
def test_start_and_stop_billable():
    category = TimeRecordCategoryFactory(billable=True)
    ticket = TicketFactory()
    user = UserFactory()
    time_record = TimeRecord.objects.start(ticket, user, category)
    assert time_record.billable is True


@pytest.mark.django_db
def test_start_and_stop_too_many():
    user = UserFactory()
    TimeRecordFactory(user=user, end_time=None)
    TimeRecordFactory(user=user, end_time=None)
    category = TimeRecordCategoryFactory()
    ticket = TicketFactory()
    with pytest.raises(InvoiceError) as e:
        TimeRecord.objects.start(ticket, user, category)
    assert 'Cannot start a time record when 2 are already' in str(e.value)


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
