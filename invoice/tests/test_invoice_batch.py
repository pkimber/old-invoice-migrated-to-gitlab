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
