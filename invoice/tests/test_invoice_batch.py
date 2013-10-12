from datetime import datetime

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceCreateBatch,
)
from crm.tests.scenario import (
    contact_contractor,
)
from invoice.tests.scenario import (
    time_fencing,
    time_paperwork_no_charge,
    invoice_settings,
)
from login.tests.scenario import (
    get_user_staff,
    user_contractor,
    user_default,
)


class TestInvoiceCreateBatch(TestCase):

    def setUp(self):
        user_contractor()
        user_default()
        contact_contractor()
        invoice_settings()
        time_fencing()
        time_paperwork_no_charge()

    def test_create_invoices(self):
        """Create an invoice"""
        InvoiceCreateBatch().create(get_user_staff(), datetime(2012, 9, 30))
        invoices = Invoice.objects.all()
        self.assertEquals(1, len(invoices))
        invoice = invoices[0]
        self.assertEquals(2, len(invoice.invoiceline_set.all()))

    def test_create_invoices_only_billable_time(self):
        """Create an invoice"""
        InvoiceCreateBatch().create(get_user_staff(), datetime(2012, 9, 30))
        self.assertEquals(
            0,
            Invoice.objects.filter(contact__slug='smallholding').count()
        )

    def test_create_invoices_do_not_bill_twice(self):
        """Check we can't include the time records more than once"""
        InvoiceCreateBatch().create(get_user_staff(), datetime(2012, 9, 30))
        self.assertEquals(1, Invoice.objects.all().count())
        InvoiceCreateBatch().create(get_user_staff(), datetime(2012, 9, 30))
        self.assertEquals(1, Invoice.objects.all().count())
