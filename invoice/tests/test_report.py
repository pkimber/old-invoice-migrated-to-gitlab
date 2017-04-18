# -*- encoding: utf-8 -*-
"""
Test report.
"""
import pytest
import pytz

from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.utils import timezone

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from invoice.models import TimeRecord
from invoice.report import (
    time_summary,
    time_summary_by_user,
    time_summary_by_user_for_chartist,
)
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_report_charge_non_charge():
    to_date = timezone.now()
    from_date = to_date + relativedelta(months=-1)
    d = from_date + relativedelta(days=7)
    TimeRecordFactory(
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
    )
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
    )
    # do not include this record - no end time
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(11, 0),
        end_time=None,
    )
    # do not include this record - outside of time
    TimeRecordFactory(
        billable=False,
        date_started=timezone.now() + relativedelta(months=+1),
        start_time=time(11, 0),
        end_time=time(11, 30),
    )
    data = TimeRecord.objects.report_charge_non_charge(from_date, to_date)
    assert {'Chargeable': 30, 'Non-Chargeable': 15} == data


@pytest.mark.django_db
def test_report_charge_non_charge_user():
    to_date = timezone.now()
    from_date = to_date + relativedelta(months=-1)
    d = from_date + relativedelta(days=7)
    user = UserFactory()
    TimeRecordFactory(
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 10),
        user=user,
    )
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 5),
        user=user,
    )
    # records for other users
    TimeRecordFactory(
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
    )
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
    )
    # do not include this record
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(11, 0),
        end_time=None,
    )
    data = TimeRecord.objects.report_charge_non_charge(
        from_date,
        to_date,
        user,
    )
    assert {'Chargeable': 10, 'Non-Chargeable': 5} == data


@pytest.mark.django_db
def test_report_time_by_contact():
    to_date = timezone.now()
    from_date = to_date + relativedelta(months=-1)
    d = from_date + relativedelta(days=7)
    ticket = TicketFactory(contact=ContactFactory(slug='bob'))
    TimeRecordFactory(
        ticket=ticket,
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
    )
    ticket = TicketFactory(contact=ContactFactory(slug='sam'))
    TimeRecordFactory(
        ticket=ticket,
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
    )
    data = TimeRecord.objects.report_time_by_contact(from_date, to_date)
    assert {'bob': 30, 'sam': 15} == data


@pytest.mark.django_db
def test_report_time_by_contact_user():
    user = UserFactory()
    to_date = timezone.now()
    from_date = to_date + relativedelta(months=-1)
    d = from_date + relativedelta(days=7)
    bob = TicketFactory(contact=ContactFactory(slug='bob'))
    sam = TicketFactory(contact=ContactFactory(slug='sam'))
    # these time records are for a different user, so exclude them
    TimeRecordFactory(
        ticket=bob,
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
    )
    TimeRecordFactory(
        ticket=sam,
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
    )
    # include these time records
    TimeRecordFactory(
        ticket=bob,
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    TimeRecordFactory(
        ticket=sam,
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
        user=user,
    )
    data = TimeRecord.objects.report_time_by_contact(from_date, to_date, user)
    assert {'bob': 30, 'sam': 15} == data


@pytest.mark.django_db
def test_report_time_by_user():
    green = UserFactory(username='green')
    red = UserFactory(username='red')
    to_date = timezone.now()
    from_date = to_date + relativedelta(months=-1)
    d = from_date + relativedelta(days=7)
    TimeRecordFactory(
        billable=True,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=red,
    )
    TimeRecordFactory(
        billable=False,
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
        user=green,
    )
    data = TimeRecord.objects.report_time_by_user(from_date, to_date)
    assert {'red': 30, 'green': 15} == data


@pytest.mark.django_db
def test_report_time_by_ticket():
    user = UserFactory(username='green')
    d = timezone.now().date()
    t1 = TicketFactory(pk=1, contact=ContactFactory())
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    TimeRecordFactory(
        ticket=TicketFactory(pk=2, contact=ContactFactory()),
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
        user=user,
    )
    # another date (so not included)
    TimeRecordFactory(
        ticket=t1,
        date_started=d+relativedelta(days=-1),
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=UserFactory(),
    )
    # another user (so not included)
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=UserFactory(),
    )
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=user,
    )
    data = TimeRecord.objects.report_time_by_ticket(user, d)
    assert {
        1: {'Chargeable': 40.0, 'Fixed-Price': 0, 'Non-Chargeable': 0},
        2: {'Chargeable': 15.0, 'Fixed-Price': 0, 'Non-Chargeable': 0},
    } == data


@pytest.mark.django_db
def test_report_time_by_user_by_week():
    user = UserFactory(username='green')
    from_date = datetime(2015, 12, 20, 0, 0, 0, tzinfo=pytz.utc)
    to_date = datetime(2016, 1, 7, 0, 0, 0, tzinfo=pytz.utc)
    TimeRecordFactory(
        billable=True,
        date_started=datetime(2015, 12, 21, 6, 0, 0, tzinfo=pytz.utc),
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    TimeRecordFactory(
        billable=True,
        date_started=datetime(2016, 1, 5, 6, 0, 0, tzinfo=pytz.utc),
        start_time=time(10, 0),
        end_time=time(10, 3),
        user=user,
    )
    TimeRecordFactory(
        billable=True,
        date_started=datetime(2016, 1, 7, 6, 0, 0, tzinfo=pytz.utc),
        start_time=time(10, 0),
        end_time=time(10, 4),
        user=UserFactory(),
    )
    TimeRecordFactory(
        billable=False,
        date_started=datetime(2016, 1, 6, 6, 0, 0, tzinfo=pytz.utc),
        start_time=time(10, 0),
        end_time=time(10, 15),
        user=user,
    )
    data = TimeRecord.objects.report_time_by_user_by_week(
        from_date, to_date, user
    )
    assert {
        '2015_51': 30,
        '2015_52': 0,
        '2016_01': 18,
        '2016_02': 0,
    } == data


@pytest.mark.django_db
def test_report_total_by_user():
    contact = ContactFactory()
    invoice = InvoiceFactory(contact=contact)
    InvoiceSettingsFactory()
    # no time records
    InvoiceLineFactory(invoice=invoice)
    # u1's time records
    invoice_line = InvoiceLineFactory(invoice=invoice)
    t1 = TicketFactory(contact=contact)
    TimeRecordFactory(
        ticket=t1,
        user=UserFactory(username='u1'),
        invoice_line=invoice_line
    )
    # u2's time records
    invoice_line = InvoiceLineFactory(invoice=invoice)
    u2 = UserFactory(username='u2')
    t2 = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=t2, user=u2, invoice_line=invoice_line)
    invoice_line = InvoiceLineFactory(invoice=invoice)
    t3 = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=t3, user=u2, invoice_line=invoice_line)
    result = invoice.time_analysis()
    # invoice has a line with no time records
    assert '' in result
    # fred recorded time on one ticket
    assert 'u1' in result
    u1 = result['u1']
    assert 1 == len(u1)
    assert t1.pk in u1
    # sara recorded time on two tickets
    assert 'u2' in result
    u2 = result['u2']
    assert 2 == len(u2)
    assert t2.pk in u2
    assert t3.pk in u2
    # web user added an invoice line, but didn't record time
    assert 'web' not in result
    # check net total matches invoice
    net = Decimal()
    for user, tickets in result.items():
        for ticket_pk, totals in tickets.items():
            net = net + totals['net']
    assert invoice.net == net


@pytest.mark.django_db
def test_time_summary():
    user = UserFactory(username='green', first_name='P', last_name='Kimber')
    d = date(2017, 4, 16)
    contact = ContactFactory(
        user=UserFactory(username='orange', first_name='O', last_name='Rind')
    )
    t1 = TicketFactory(pk=1, contact=ContactFactory(user=user))
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    contact = ContactFactory(
        user=UserFactory(username='blue', first_name='A', last_name='Teal')
    )
    TimeRecordFactory(
        ticket=TicketFactory(pk=2, contact=contact),
        date_started=d,
        start_time=time(10, 0),
        end_time=time(10, 15),
        user=user,
    )
    # another date (so not included)
    TimeRecordFactory(
        ticket=t1,
        date_started=d+relativedelta(days=-1),
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=UserFactory(),
    )
    # another user (so not included)
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=UserFactory(),
    )
    TimeRecordFactory(
        ticket=t1,
        date_started=d,
        start_time=time(12, 0),
        end_time=time(12, 10),
        user=user,
    )
    data = time_summary(user)
    assert {
        date(2017, 4, 16): {
            'tickets': [
                {
                    'analysis': {
                        'charge_minutes': 40.0,
                        'charge_minutes_format': '00:40',
                        'fixed_minutes': 0,
                        'fixed_minutes_format': '00:00',
                        'non_minutes': 0,
                        'non_minutes_format': '00:00'
                    },
                    'contact': 'P Kimber',
                    'description': '',
                    'pk': 1,
                    'user_name': 'green'
                },
                {
                    'analysis': {
                        'charge_minutes': 15.0,
                        'charge_minutes_format': '00:15',
                        'fixed_minutes': 0,
                        'fixed_minutes_format': '00:00',
                        'non_minutes': 0,
                        'non_minutes_format': '00:00'
                    },
                    'contact': 'A Teal',
                    'description': '',
                    'pk': 2,
                    'user_name': 'blue'
                }
            ],
            'total': 55.0,
            'total_format': '00:55',
            'total_charge': 55.0,
            'total_charge_format': '00:55',
            'total_fixed': 0,
            'total_fixed_format': '00:00',
            'total_non': 0,
            'total_non_format': '00:00',
        }
    } == data


@pytest.mark.django_db
def test_time_summary_by_user():
    user = UserFactory(username='green', first_name='P', last_name='Kimber')
    contact = ContactFactory(user=user)
    TimeRecordFactory(
        ticket=TicketFactory(contact=contact),
        date_started=date(2017, 1, 16),
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    TimeRecordFactory(
        billable=False,
        ticket=TicketFactory(contact=contact),
        date_started=date(2016, 12, 1),
        start_time=time(11, 0),
        end_time=time(11, 15),
        user=user,
    )
    TimeRecordFactory(
        ticket=TicketFactory(contact=contact, fixed_price=True),
        date_started=date(2016, 11, 30),
        start_time=time(11, 0),
        end_time=time(11, 10),
        user=user,
    )
    data = time_summary_by_user(date(2017, 3, 17))
    assert {
        'green': {
            '2016-03': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Mar',
                'month': 3,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-04': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Apr',
                'month': 4,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-05': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'May',
                'month': 5,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-06': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Jun',
                'month': 6,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-07': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Jul',
                'month': 7,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-08': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Aug',
                'month': 8,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-09': {
                 'charge_minutes': 0,
                 'fixed_minutes': 0,
                 'label': 'Sep',
                 'month': 9,
                 'non_minutes': 0,
                 'year': 2016,
            },
            '2016-10': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Oct',
                'month': 10,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-11': {
                'charge_minutes': 0,
                'fixed_minutes': 10,
                'label': 'Nov',
                'month': 11,
                'non_minutes': 0,
                'year': 2016,
            },
            '2016-12': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Dec',
                'month': 12,
                'non_minutes': 15,
                'year': 2016,
            },
            '2017-01': {
                'charge_minutes': 30.0,
                'fixed_minutes': 0,
                'label': 'Jan',
                'month': 1,
                'non_minutes': 0,
                'year': 2017,
            },
            '2017-02': {
                'charge_minutes': 0,
                'fixed_minutes': 0,
                'label': 'Feb',
                'month': 2,
                'non_minutes': 0,
                'year': 2017,
            },
        }
    } == data


@pytest.mark.django_db
def test_time_summary_by_user_for_chartist():
    user = UserFactory(username='green', first_name='P', last_name='Kimber')
    contact = ContactFactory()
    TimeRecordFactory(
        ticket=TicketFactory(contact=contact),
        date_started=date(2017, 1, 16),
        start_time=time(11, 0),
        end_time=time(11, 30),
        user=user,
    )
    TimeRecordFactory(
        billable=False,
        ticket=TicketFactory(contact=contact),
        date_started=date(2016, 12, 1),
        start_time=time(11, 0),
        end_time=time(11, 15),
        user=user,
    )
    TimeRecordFactory(
        ticket=TicketFactory(contact=contact, fixed_price=True),
        date_started=date(2016, 11, 30),
        start_time=time(11, 0),
        end_time=time(11, 10),
        user=user,
    )
    assert {
        'green': {
            'labels': [
                'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb',
            ],
            'series': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0],
            ],
        }
    } == time_summary_by_user_for_chartist(date(2017, 3, 17))
