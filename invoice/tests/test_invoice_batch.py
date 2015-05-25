# -*- encoding: utf-8 -*-
from datetime import date

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceCreateBatch,
)
from crm.tests.factories import (
    ContactFactory,
    TicketFactory,
)
from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
)
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
#from invoice.tests.scenario import default_scenario_invoice
from login.tests.factories import UserFactory
from login.tests.scenario import (
    default_scenario_login,
    get_user_staff,
    user_contractor,
)


class TestInvoiceCreateBatch(TestCase):

    #def setUp(self):
    #    user_contractor()
    #    default_scenario_login()
    #    default_scenario_crm()
    #    default_scenario_invoice()

    def test_create_invoices(self):
        """Create an invoice"""
        InvoiceSettingsFactory()
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 8, 1))
        TimeRecordFactory(ticket=ticket)
        # action
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        invoices = Invoice.objects.filter(contact=contact)
        self.assertEquals(1, len(invoices))
        invoice = invoices[0]
        self.assertEquals(2, len(invoice.invoiceline_set.all()))

    def test_create_invoices_only_billable_time(self):
        InvoiceSettingsFactory()
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        TimeRecordFactory(
            ticket=ticket,
            date_started=date(2012, 7, 1),
            billable=False,
        )
        InvoiceCreateBatch().create(UserFactory(), date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )

    def test_create_invoices_do_not_bill_twice(self):
        """Check we can't include the time records more than once"""
        InvoiceSettingsFactory()
        contact = ContactFactory()
        ticket = TicketFactory(contact=contact)
        TimeRecordFactory(ticket=ticket, date_started=date(2012, 7, 1))
        #TimeRecordFactory(ticket=ticket, date_started=date(2012, 8, 1))
        #TimeRecordFactory(ticket=ticket)
        user = UserFactory()
        InvoiceCreateBatch().create(user, date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )
        InvoiceCreateBatch().create(user, date(2012, 9, 30))
        self.assertEquals(
            1,
            Invoice.objects.filter(contact=contact).count()
        )
