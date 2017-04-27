# -*- encoding: utf-8 -*-
import pytest

from datetime import date

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from finance.tests.factories import VatSettingsFactory
from invoice.models import Invoice
from invoice.service import InvoiceCreateBatch
from invoice.tests.factories import (
    InvoiceContactFactory,
    InvoiceLine,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_create_invoices():
    """Create an invoice"""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
    TimeRecordFactory(ticket=ticket, date_started=date(2012, 8, 1))
    TimeRecordFactory(ticket=ticket)
    # action
    InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
    invoices = Invoice.objects.filter(contact=contact)
    assert 1 == len(invoices)
    invoice = invoices[0]
    assert 2 == len(invoice.invoiceline_set.all())


@pytest.mark.django_db
def test_create_invoices_only_billable_time():
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
    InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
    TimeRecordFactory(
        ticket=ticket,
        date_started=date(2012, 7, 1),
        billable=False,
    )
    InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
    assert 1 == Invoice.objects.filter(contact=contact).count()


@pytest.mark.django_db
def test_create_invoices_not_fixed_price():
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    # ticket 1
    t1 = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=t1, title='t1', date_started=date(2012, 7, 1))
    # ticket 2 is for fixed price work
    t2 = TicketFactory(contact=contact, fixed_price=True)
    TimeRecordFactory(ticket=t2, title='t2', date_started=date(2012, 7, 2))
    # ticket 3
    t3 = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=t3, title='t3', date_started=date(2012, 7, 3))
    # test
    InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
    assert 1 == Invoice.objects.filter(contact=contact).count()
    invoice = Invoice.objects.get(contact=contact)
    assert ['t1', 't3'] == [
        x.timerecord.title for x in InvoiceLine.objects.filter(invoice=invoice)
    ]


@pytest.mark.django_db
def test_create_invoices_do_not_bill_twice():
    """Check we can't include the time records more than once"""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
    user = UserFactory()
    InvoiceCreateBatch().create(user, date(2012, 9, 30))
    assert 1 == Invoice.objects.filter(contact=contact).count()
    InvoiceCreateBatch().create(user, date(2012, 9, 30))
    assert 1 == Invoice.objects.filter(contact=contact).count()
