from datetime import datetime
from datetime import time
from decimal import Decimal

from crm.tests.scenario import (
    get_contact_farm,
    get_contact_smallholding,
    get_ticket_fence_for_farm,
    get_ticket_fix_roof_for_farm,
    get_ticket_paperwork_for_smallholding,
)
from invoice.models import (
    Invoice,
    TimeRecord,
)
from invoice.tests.model_maker import (
    make_invoice,
    make_invoice_line,
    make_invoice_settings,
    make_time_record,
)
from login.tests.scenario import (
    get_user_fred,
    get_user_sara,
    get_user_staff,
    get_user_web,
)


def get_invoice_time_analysis():
    return Invoice.objects.get(
        user=get_user_staff(),
        invoice_date=datetime(2014, 2, 5),
    )


def get_invoice_paperwork():
    return Invoice.objects.get(
        user=get_user_staff(),
        invoice_date=datetime(2012, 3, 31),
    )


def get_invoice_line_paperwork_no_time():
    invoice = get_invoice_paperwork()
    return invoice.invoiceline_set.get(units='pen')


def get_invoice_line_paperwork_has_time():
    invoice = get_invoice_paperwork()
    return invoice.invoiceline_set.get(units='hours')


def get_timerecord_fence_dig_holes():
    return TimeRecord.objects.get(title='Dig holes for the corner posts')


def get_timerecord_paperwork_template():
    return TimeRecord.objects.get(title='Invoice template on Microsoft Word')


def invoice_settings():
    make_invoice_settings(
        vat_rate=Decimal('0.20'),
        vat_number='',
        name_and_address='Patrick Kimber, Hatherleigh, EX20 1AB',
        phone_number='01234 234 456',
        footer="Please pay by bank transfer<br />Thank you"
    )


def _make_line(invoice, line_number, hours, user=None):
    user = user or get_user_staff()
    return make_invoice_line(
        invoice,
        line_number,
        hours,
        'hours',
        100.00,
        0.00,
        user=user,
    )


def _make_time(invoice, line_number, ticket, hours, user):
    time_record = make_time_record(
        ticket,
        user,
        'Test Time',
        datetime(2012, 3, 4),
        time(11, 0),
        time(13, 30),
        billable=True,
    )
    time_record.invoice_line = _make_line(invoice, line_number, hours)
    time_record.save()


def default_scenario_invoice():
    invoice_settings()
    invoice = make_invoice(
        get_user_staff(),
        datetime(2014, 2, 5),
        get_contact_farm()
    )
    line_number = 0
    line_number = line_number + 1
    _make_line(invoice, line_number, 1.0, get_user_web())
    line_number = line_number + 1
    _make_line(invoice, line_number, 1.0, get_user_sara())
    line_number = line_number + 1
    _make_time(invoice, line_number, get_ticket_fence_for_farm(), 2.0, get_user_fred())
    line_number = line_number + 1
    _make_time(invoice, line_number, get_ticket_fence_for_farm(), 8.0, get_user_fred())
    line_number = line_number + 1
    _make_time(invoice, line_number, get_ticket_fence_for_farm(), 6.0, get_user_sara())
    line_number = line_number + 1
    _make_time(invoice, line_number, get_ticket_fix_roof_for_farm(), 14.0, get_user_sara())


def time_fencing():
    """fencing for the farm.  We charge Fred for all the work we do"""
    fence = get_ticket_fence_for_farm()
    staff = get_user_staff()
    make_time_record(
        fence,
        staff,
        'Work out how many fence posts to order',
        datetime(2012, 9, 1),
        time(9, 0),
        time(12, 30),
        billable=True,
    )
    make_time_record(
        fence,
        staff,
        'Move fencing equipment to the farm',
        datetime(2012, 9, 30),
        time(13, 30),
        time(15, 30),
        billable=True,
    )
    make_time_record(
        fence,
        staff,
        'Dig holes for the corner posts',
        datetime(2012, 10, 1),
        time(13, 30),
        time(15, 30),
        billable=True,
    )


def time_paperwork():
    smallholding = get_contact_smallholding()
    paper = get_ticket_paperwork_for_smallholding()
    staff = get_user_staff()
    time_record = make_time_record(
        paper,
        staff,
        'Invoice template on Microsoft Word',
        datetime(2012, 3, 4),
        time(11, 0),
        time(13, 30),
        billable=True,
    )
    invoice = make_invoice(
        staff,
        datetime(2012, 3, 31),
        smallholding,
    )
    make_invoice_line(
        invoice,
        2,
        1,
        'pen',
        1.00,
        0.0
    )
    invoice_line = make_invoice_line(
        invoice,
        1,
        2,
        'hours',
        20.00,
        0.20
    )
    time_record.invoice_line = invoice_line
    time_record.save()
    # Some non-chargeable time
    make_time_record(
        paper,
        staff,
        'Help with the VAT return',
        datetime(2012, 9, 1),
        time(9, 0),
        time(12, 30),
        billable=False,
    )
    return invoice
