# -*- encoding: utf-8 -*-
import csv
import pytest

from datetime import date, time

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from invoice.tasks import time_summary_by_user
from invoice.tests.factories import TimeRecordFactory
from login.tests.factories import UserFactory
from report.models import ReportSchedule


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
    assert 0 == ReportSchedule.objects.count()
    # test the task
    time_summary_by_user()
    assert 1 == ReportSchedule.objects.count()
    report_schedule = ReportSchedule.objects.first()
    reader = csv.reader(open(report_schedule.full_path), 'excel')
    first_row = None
    result = []
    for row in reader:
        if not first_row:
            first_row = row
        else:
            # check the values in the last three columns (dates will change)
            result.append(row[4:])
    assert [
        'user_name',
        'year',
        'month',
        'label',
        'non_minutes',
        'fixed_minutes',
        'charge_minutes',
    ] == first_row
    assert [
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '0', '0'],
        ['0', '10', '0'],
        ['15', '0', '0'],
        ['0', '0', '30'],
        ['0', '0', '0'],
        ['0', '0', '0'],
    ] == result
