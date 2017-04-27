# -*- encoding: utf-8 -*-
import pytest
import pytz

from datetime import date, datetime, time
from django.utils import timezone

from contact.tests.factories import ContactFactory
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
def test_stop():
    obj = TimeRecordFactory(end_time=None)
    assert obj.end_time is None
    obj.stop()
    assert obj.end_time is not None


@pytest.mark.django_db
def test_stop_end_time():
    obj = TimeRecordFactory(end_time=None)
    assert obj.end_time is None
    end_time = datetime(2014, 10, 1, 18, 13, 32, tzinfo=pytz.utc)
    obj.stop(end_time)
    assert end_time == obj.end_time


@pytest.mark.django_db
def test_stop_already_stopped():
    end_time = datetime(2014, 10, 1, 18, 13, 32, tzinfo=pytz.utc)
    obj = TimeRecordFactory(end_time=end_time)
    with pytest.raises(InvoiceError) as e:
        obj.stop()
    assert 'has already been stopped' in str(e.value)


@pytest.mark.django_db
def test_str():
    time_record = TimeRecordFactory()
    str(time_record)


@pytest.mark.django_db
def test_tickets():
    """List of tickets where time was recorded for a user."""
    user = UserFactory()
    today = date.today()
    # first day of the month
    from_date = today + relativedelta(day=1)
    # last day of the month
    to_date = today + relativedelta(months=+1, day=1, days=-1)
    # last month
    last_month = today + relativedelta(months=-1)
    # next month
    next_month = today + relativedelta(months=+1)
    TimeRecordFactory(
        ticket=TicketFactory(title='t0'),
        user=user,
        date_started=last_month,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t1'),
        user=user,
        date_started=from_date,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t2'),
        user=user,
        date_started=today,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t3'),
        date_started=to_date,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t4'),
        user=user,
        date_started=to_date,
        end_time=None,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t5'),
        user=user,
        date_started=to_date,
    )
    TimeRecordFactory(
        ticket=TicketFactory(title='t6'),
        user=user,
        date_started=next_month,
    )
    qs = TimeRecord.objects.tickets(from_date, to_date, user)
    assert ['t1', 't2', 't5'] == [x.title for x in qs]


@pytest.mark.django_db
def test_to_invoice():
    contact = ContactFactory()
    d = date(2012, 7, 1)
    #
    TimeRecordFactory(
        title='t1',
        ticket=TicketFactory(contact=contact),
        date_started=d,
    )
    # exclude records created after the invoice date
    TimeRecordFactory(
        title='t2',
        ticket=TicketFactory(contact=contact),
        date_started=date(2012, 8, 1),
    )
    # exclude records for another contact
    TimeRecordFactory(
        title='t3',
        ticket=TicketFactory(contact=ContactFactory()),
        date_started=d,
    )
    # exclude records which have already been invoiced
    TimeRecordFactory(
        title='t4',
        ticket=TicketFactory(contact=contact),
        date_started=d,
        invoice_line=InvoiceLineFactory(),
    )
    # exclude records which have a fixed price ticket
    TimeRecordFactory(
        title='t5',
        ticket=TicketFactory(contact=contact, fixed_price=True),
        date_started=d,
    )
    #
    TimeRecordFactory(
        title='t6',
        ticket=TicketFactory(contact=contact),
        date_started=d,
    )
    qs = TimeRecord.objects.to_invoice(contact, date(2012, 7, 31))
    assert ['t1', 't6'] == [x.title for x in qs]


@pytest.mark.django_db
def test_user_can_edit():
    time_record = TimeRecordFactory()
    assert time_record.user_can_edit is True


@pytest.mark.django_db
def test_user_can_edit_invoice_line():
    invoice_line = InvoiceLineFactory()
    time_record = TimeRecordFactory(invoice_line=invoice_line)
    assert time_record.user_can_edit is False
