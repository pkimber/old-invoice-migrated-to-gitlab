# -*- encoding: utf-8 -*-
import pytest

from datetime import date
from decimal import Decimal

from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from finance.tests.factories import VatSettingsFactory
from invoice.service import (
    InvoiceCreate,
    InvoiceError,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceContactFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)


@pytest.mark.django_db
def test_invoice_with_time_records():
    """Invoice time records."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    tr1 = TimeRecordFactory(ticket=ticket)
    TimeRecordFactory(ticket=ticket)
    invoice = InvoiceCreate().create(
        tr1.user, contact, date.today()
    )
    assert invoice.is_draft
    InvoicePrint().create_pdf(invoice, None)
    assert not invoice.is_draft
    assert Decimal('40.00') == invoice.net


@pytest.mark.django_db
def test_invoice_with_time_records_no_end_time():
    """One of the time records has no end time, so cannot be invoiced."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    tr1 = TimeRecordFactory(ticket=ticket)
    TimeRecordFactory(ticket=ticket, end_time=None)
    TimeRecordFactory(ticket=ticket)
    with pytest.raises(InvoiceError) as ex:
        InvoiceCreate().create(tr1.user, contact, date.today())
    message = str(ex.value)
    assert 'does not have a' in message
    assert 'end time' in message
