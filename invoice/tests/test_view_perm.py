# -*- encoding: utf-8 -*-
import pytest

from datetime import date

from django.core.urlresolvers import reverse

from base.tests.test_utils import PermTestCase
from contact.tests.factories import ContactFactory
from crm.tests.factories import TicketFactory
from finance.tests.factories import VatSettingsFactory
from invoice.service import (
    InvoiceCreate,
    InvoicePrint,
)
from invoice.tests.factories import (
    InvoiceContactFactory,
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    QuickTimeRecordFactory,
    TimeRecordFactory,
)
from login.tests.factories import UserFactory
from login.tests.fixture import perm_check


@pytest.mark.django_db
def test_contact_invoice_list(perm_check):
    contact = ContactFactory()
    url = reverse('invoice.contact.list', kwargs={'pk': contact.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_contact_time_record_list(perm_check):
    contact = ContactFactory()
    url = reverse('invoice.time.contact.list', kwargs={'pk': contact.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_contact_create(perm_check):
    contact = ContactFactory()
    url = reverse('invoice.contact.create', kwargs={'pk': contact.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_contact_update(perm_check):
    contact = ContactFactory()
    invoice_contact = InvoiceContactFactory(contact=contact)
    url = reverse(
        'invoice.contact.update',
        kwargs={'pk': invoice_contact.pk}
    )
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_create_draft(perm_check):
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    url = reverse('invoice.create.draft', kwargs={'pk': contact.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_create_time(perm_check):
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    url = reverse('invoice.create.time', kwargs={'pk': contact.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_list(perm_check):
    url = reverse('invoice.list')
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_download(perm_check):
    InvoiceSettingsFactory()
    VatSettingsFactory()
    contact = ContactFactory()
    InvoiceContactFactory(contact=contact)
    ticket = TicketFactory(contact=contact)
    TimeRecordFactory(ticket=ticket, date_started=date(2013, 12, 1))
    invoice = InvoiceCreate().create(
        UserFactory(),
        contact,
        date(2013, 12, 31)
    )
    InvoicePrint().create_pdf(invoice, header_image=None)
    url = reverse('invoice.download', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_detail(perm_check):
    invoice = InvoiceFactory()
    url = reverse('invoice.detail', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_line_create(perm_check):
    invoice = InvoiceFactory()
    url = reverse('invoice.line.create', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_line_update(perm_check):
    invoice = InvoiceFactory()
    InvoiceLineFactory(invoice=invoice)
    url = reverse('invoice.line.update', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_create_pdf(perm_check):
    invoice = InvoiceFactory()
    url = reverse('invoice.create.pdf', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_update(perm_check):
    invoice = InvoiceFactory()
    url = reverse('invoice.update', kwargs={'pk': invoice.pk})
    perm_check.staff(url)


@pytest.mark.django_db
def test_invoice_user_update(perm_check):
    url = reverse('invoice.user.update')
    perm_check.staff(url)


@pytest.mark.django_db
def test_quick_time_record(perm_check):
    perm_check.staff(reverse('invoice.quick.time.record.list'))


@pytest.mark.django_db
def test_quick_time_record_create(perm_check):
    perm_check.staff(reverse('invoice.quick.time.record.create'))


@pytest.mark.django_db
def test_quick_time_record_delete(perm_check):
    obj = QuickTimeRecordFactory()
    perm_check.staff(reverse('invoice.quick.time.record.delete', args=[obj.pk]))


@pytest.mark.django_db
def test_quick_time_record_update(perm_check):
    obj = QuickTimeRecordFactory()
    perm_check.staff(reverse('invoice.quick.time.record.update', args=[obj.pk]))


@pytest.mark.django_db
def test_timerecord_list(perm_check):
    url = reverse('invoice.time')
    perm_check.staff(url)


@pytest.mark.django_db
def test_timerecord_summary(perm_check):
    url = reverse('invoice.time.summary')
    perm_check.staff(url)


@pytest.mark.django_db
def test_timerecord_summary_user(perm_check):
    user = UserFactory()
    url = reverse('invoice.time.summary.user', args=[user.pk])
    perm_check.staff(url)


@pytest.mark.django_db
def test_timerecord_create(perm_check):
    ticket = TicketFactory()
    url = reverse(
        'invoice.time.create',
        kwargs={'pk': ticket.pk}
    )
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_list_month(perm_check):
    url = reverse('invoice.ticket.list.month', args=[2000, 3])
    perm_check.staff(url)


@pytest.mark.django_db
def test_ticket_timerecord_list(perm_check):
    ticket = TicketFactory()
    url = reverse(
        'invoice.time.ticket.list',
        kwargs={'pk': ticket.pk}
    )
    perm_check.staff(url)


@pytest.mark.django_db
def test_user_timerecord_list(perm_check):
    url = reverse('invoice.time.user.list')
    perm_check.staff(url)


@pytest.mark.django_db
def test_timerecord_update(perm_check):
    time_record = TimeRecordFactory()
    url = reverse(
        'invoice.time.update',
        kwargs={'pk': time_record.pk}
    )
    perm_check.staff(url)
