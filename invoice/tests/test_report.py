# -*- encoding: utf-8 -*-
"""
Test report.
"""
import pytest

from decimal import Decimal

from django.test import TestCase

from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


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
