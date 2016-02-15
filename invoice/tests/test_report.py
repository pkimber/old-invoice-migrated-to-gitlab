# -*- encoding: utf-8 -*-
"""
Test report.
"""
import pytest

from datetime import time
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.utils import timezone

from crm.tests.factories import (
    # ContactFactory,
    TicketFactory,
)
from invoice.models import TimeRecord
from invoice.service import report
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory
from report.models import (
    Report,
    ReportDataInteger,
)


@pytest.mark.django_db
def test_reports():
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
    report()
    obj = Report.objects.get(slug='invoice_charge_non_charge')
    qs = ReportDataInteger.objects.filter(report=obj)
    assert 2 == qs.count()


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


