from datetime import datetime
from datetime import time
from decimal import Decimal

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceCreateBatch,
    VAT_RATE,
)
from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
)
from invoice.tests.model_maker import (
    make_time_record,
)
from login.tests.model_maker import make_user


class TestInvoiceCreateBatch(TestCase):

    def setUp(self):
        self.user = make_user('fred')

    def _set_up_test_data(self, billable):
        """ Create a project with a task and time records """
        tom = make_user('tom')
        icl = make_contact('icl', 'ICL', hourly_rate=Decimal('20.00'))
        ticket = make_ticket(
            icl,
            tom,
            'Sew',
            make_priority('Low', 1),
        )
        make_time_record(
            ticket,
            tom,
            'Make a pillow case',
            datetime(2012, 9, 1),
            time(9, 0),
            time(12, 30),
            billable
        )
        # time record is on the day of the iteration end date
        make_time_record(
            ticket,
            tom,
            'Buy a new sewing machine',
            datetime(2012, 9, 30),
            time(13, 30),
            time(15, 30),
            billable
        )
        # time record is after the iteration end date so should not be included
        make_time_record(
            ticket,
            tom,
            'Enter in the local show',
            datetime(2012, 10, 1),
            time(13, 30),
            time(15, 30),
            billable
        )

    def test_create_invoices(self):
        """
        Create a project with a task and time records.  Create an invoice.
        """
        self._set_up_test_data(billable=True)
        InvoiceCreateBatch(VAT_RATE, datetime(2012, 9, 30)).create()
        invoices = Invoice.objects.all()
        self.assertEquals(1, len(invoices))
        invoice = invoices[0]
        self.assertEquals(2, len(invoice.invoiceline_set.all()))

    def test_create_invoices_only_billable_time(self):
        """
        Create a project with a task and time records.  Create an invoice.
        """
        self._set_up_test_data(billable=False)
        InvoiceCreateBatch(VAT_RATE, datetime(2012, 9, 30)).create()
        self.assertEquals(0, Invoice.objects.all().count())

    def test_create_invoices_do_not_bill_twice(self):
        """
        Create a project with a task and time records.  Check we can't include
        the time records more than once.
        """
        self._set_up_test_data(billable=True)
        InvoiceCreateBatch(VAT_RATE, datetime(2012, 9, 30)).create()
        self.assertEquals(1, Invoice.objects.all().count())
        InvoiceCreateBatch(VAT_RATE, datetime(2012, 9, 30)).create()
        self.assertEquals(1, Invoice.objects.all().count())
