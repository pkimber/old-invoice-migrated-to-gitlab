# -*- encoding: utf-8 -*-
"""
Test report.
"""
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


class TestReport(TestCase):

    def test_report_total_by_user(self):
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
        self.assertIn('', result)
        # fred recorded time on one ticket
        self.assertIn('u1', result)
        u1 = result['u1']
        self.assertEqual(1, len(u1))
        self.assertIn(t1.pk, u1)
        # sara recorded time on two tickets
        self.assertIn('u2', result)
        u2 = result['u2']
        self.assertEqual(2, len(u2))
        self.assertIn(t2.pk, u2)
        self.assertIn(t3.pk, u2)
        # web user added an invoice line, but didn't record time
        self.assertNotIn('web', result)
        # check net total matches invoice
        net = Decimal()
        for user, tickets in result.items():
            for ticket_pk, totals in tickets.items():
                net = net + totals['net']
        self.assertEqual(invoice.net, net)
