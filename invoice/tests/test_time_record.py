# -*- encoding: utf-8 -*-
"""
Test time records.
"""
import pytest

from datetime import time
from django.utils import timezone

from crm.tests.factories import TicketFactory
from dateutil.relativedelta import relativedelta
from invoice.models import InvoiceError, TimeRecord
from invoice.tests.factories import (
    InvoiceLineFactory,
    TimeRecordFactory,
    QuickTimeRecordFactory,
)
from login.tests.factories import UserFactory
from search.tests.helper import check_search_methods


@pytest.mark.django_db
def test_is_today():
    obj = TimeRecordFactory(date_started=timezone.now().date())
    assert obj.is_today() is True


@pytest.mark.django_db
def test_is_today_not():
    d = timezone.now().date() + relativedelta(days=-7)
    obj = TimeRecordFactory(date_started=d)
    assert obj.is_today() is False


@pytest.mark.django_db
def test_running():
    user = UserFactory()
    t1 = TimeRecordFactory(title='t1', user=user, end_time=None)
    t2 = TimeRecordFactory(title='t2', user=user, end_time=time(11, 0))
    d = timezone.now().date() + relativedelta(days=-7)
    t3 = TimeRecordFactory(title='t3', date_started=d, user=user, end_time=None)
    t4 = TimeRecordFactory(title='t4', user=UserFactory(), end_time=None)
    qs = TimeRecord.objects.running(user).order_by('title')
    assert ['t1', 't3'] == [obj.title for obj in qs]


@pytest.mark.django_db
def test_running_today():
    user = UserFactory()
    t1 = TimeRecordFactory(title='t1', user=user, end_time=None)
    t2 = TimeRecordFactory(title='t2', user=user, end_time=time(11, 0))
    d = timezone.now().date() + relativedelta(days=7)
    t3 = TimeRecordFactory(title='t3', date_started=d, user=user, end_time=None)
    t4 = TimeRecordFactory(title='t4', user=UserFactory(), end_time=None)
    qs = TimeRecord.objects.running_today(user).order_by('title')
    assert ['t1'] == [obj.title for obj in qs]


@pytest.mark.django_db
def test_search_methods():
    time_record = TimeRecordFactory()
    check_search_methods(time_record)


@pytest.mark.django_db
def test_start():
    user = UserFactory()
    quick = QuickTimeRecordFactory(user=user)
    ticket = TicketFactory()
    time_record = TimeRecord.objects.start(ticket, quick)
    assert quick.time_code == time_record.time_code
    assert ticket == time_record.ticket
    assert time_record.end_time is None
    assert time_record.start_time is not None
    assert quick.user == time_record.user


@pytest.mark.django_db
def test_start_and_stop():
    user = UserFactory()
    running = TimeRecordFactory(user=user, end_time=None)
    assert running.end_time is None
    quick = QuickTimeRecordFactory(user=user)
    ticket = TicketFactory()
    time_record = TimeRecord.objects.start(ticket, quick)
    assert quick.time_code == time_record.time_code
    assert quick.description == time_record.title
    assert time_record.billable is False
    assert time_record.end_time is None
    assert time_record.start_time is not None
    assert user == time_record.user
    running.refresh_from_db()
    assert running.end_time == time_record.start_time


@pytest.mark.django_db
def test_start_and_stop_billable():
    quick = QuickTimeRecordFactory(chargeable=True)
    ticket = TicketFactory()
    time_record = TimeRecord.objects.start(ticket, quick)
    assert time_record.billable is True


@pytest.mark.django_db
def test_start_and_stop_too_many():
    user = UserFactory()
    TimeRecordFactory(user=user, end_time=None)
    TimeRecordFactory(user=user, end_time=None)
    quick = QuickTimeRecordFactory(user=user)
    ticket = TicketFactory()
    with pytest.raises(InvoiceError) as e:
        TimeRecord.objects.start(ticket, quick)
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
