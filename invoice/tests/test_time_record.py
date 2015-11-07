# -*- encoding: utf-8 -*-
"""
Test time records.
"""
import pytest

from datetime import time
from dateutil.relativedelta import relativedelta

from django.test import TestCase
from django.utils import timezone

from invoice.models import TimeRecord
from invoice.tests.factories import (
    InvoiceLineFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory
from search.tests.helper import check_search_methods


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
    x, y = TimeRecord.objects.report_charge_non_charge(from_date, to_date)
    assert ['Chargeable', 'Non-Chargeable'] == x
    assert [30, 15] == y


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
    x, y = TimeRecord.objects.report_charge_non_charge(
        from_date,
        to_date,
        user,
    )
    assert ['Chargeable', 'Non-Chargeable'] == x
    assert [10, 5] == y


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
