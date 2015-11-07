# -*- encoding: utf-8 -*-
import pytest

from datetime import date
from dateutil.relativedelta import relativedelta

from finance.tests.factories import VatSettingsFactory
from invoice.models import InvoiceError
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)

@pytest.mark.django_db
def test_is_not_draft():
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    assert invoice.is_draft is True
    InvoicePrint().create_pdf(invoice, None)
    assert invoice.is_draft is False


@pytest.mark.django_db
def test_set_is_draft():
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    assert invoice.is_draft is True
    InvoicePrint().create_pdf(invoice, None)
    assert invoice.is_draft is False
    invoice.set_to_draft()
    assert invoice.is_draft is True


@pytest.mark.django_db
def test_set_is_draft_too_late():
    """invoice can only be set back to draft on the day it is created."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    TimeRecordFactory(ticket = tr.ticket)
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    invoice.invoice_date=date.today() + relativedelta(days=-1)
    invoice.save()
    assert invoice.is_draft is True
    InvoicePrint().create_pdf(invoice, None)
    assert invoice.is_draft is False
    with pytest.raises(InvoiceError) as e:
        invoice.set_to_draft()
    assert 'only set an invoice back to draft on the day' in str(e.value)


@pytest.mark.django_db
def test_remove_time_lines():
    """Remove all lines (because they are all linked to time records)."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    TimeRecordFactory(ticket=tr.ticket)
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    assert invoice.is_draft is True
    InvoicePrint().create_pdf(invoice, None)
    assert invoice.has_lines is True
    invoice.set_to_draft()
    invoice.remove_time_lines()
    assert invoice.has_lines is False


@pytest.mark.django_db
def test_remove_time_lines_not_extra():
    """Remove all but one line.

    The extra line is not removed because it isn't linked to a time record.

    .. important:: This test will fail if you try to run it around midnight.
                   The end time will be something like ``time(0, 45)`` and
                   the start time will be something like ``time(23, 45)``.
                   Both are for the same date, and the end date will look as if
                   it is before the start date!

    """
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    TimeRecordFactory(ticket=tr.ticket)
    invoice = InvoiceCreate().create(
        tr.user,
        tr.ticket.contact,
        date.today()
    )
    extra_line = InvoiceLineFactory(invoice=invoice)
    assert invoice.is_draft is True
    InvoicePrint().create_pdf(invoice, None)
    assert invoice.has_lines is True
    invoice.set_to_draft()
    invoice.remove_time_lines()
    assert [extra_line.pk] == [i.pk for i in invoice.invoiceline_set.all()]


@pytest.mark.django_db
def test_refresh():
    """Create a draft invoice, and then add more time records to it."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    assert 1 == invoice.invoiceline_set.count()
    # create a couple more time records which can be added
    TimeRecordFactory(ticket=tr.ticket)
    TimeRecordFactory(ticket=tr.ticket)
    InvoiceCreate().refresh(tr.user, invoice, date.today())
    assert 3 == invoice.invoiceline_set.count()


@pytest.mark.django_db
def test_refresh_draft_only():
    """Only draft invoices can be refreshed."""
    InvoiceSettingsFactory()
    VatSettingsFactory()
    tr = TimeRecordFactory()
    invoice = InvoiceCreate().create(
        tr.user, tr.ticket.contact, date.today()
    )
    assert 1 == invoice.invoiceline_set.count()
    InvoicePrint().create_pdf(invoice, None)
    with pytest.raises(InvoiceError) as e:
        InvoiceCreate().refresh(tr.user, invoice, date.today())
    assert 'Time records can only be added to a draft invoice' in str(e.value)
