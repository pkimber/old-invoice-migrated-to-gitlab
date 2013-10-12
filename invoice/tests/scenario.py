from datetime import datetime
from datetime import time
from decimal import Decimal

from crm.tests.scenario import (
    get_ticket_fence_for_fred,
    get_ticket_paperwork_for_sara,
)
from invoice.tests.model_maker import (
    make_invoice_settings,
    make_time_record,
)
from login.tests.scenario import (
    get_user_fred,
    get_user_sara,
    get_user_staff,
)


def invoice_settings():
    make_invoice_settings(
        vat_rate=Decimal('0.20'),
        vat_number='',
        name_and_address='Patrick Kimber, Hatherleigh, EX20 1AB',
        phone_number='01234 234 456',
        footer="Please pay by bank transfer<br />Thank you"
    )


def time_fencing():
    """this fencing is for Fred's farm.  We charge him for all the work we do"""
    fence = get_ticket_fence_for_fred()
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


def time_paperwork_no_charge():
    paper = get_ticket_paperwork_for_sara()
    staff = get_user_staff()
    make_time_record(
        paper,
        staff,
        'Help with the VAT return',
        datetime(2012, 9, 1),
        time(9, 0),
        time(12, 30),
        billable=False,
    )
