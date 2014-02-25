# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
"""
Test report.
"""
from datetime import datetime
from datetime import time
from decimal import Decimal

from django.test import TestCase

from crm.tests.scenario import default_scenario_crm
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)

from invoice.models import Invoice
from invoice.tests.scenario import (
    default_scenario_invoice,
    get_invoice_time_analysis,
)


class TestReport(TestCase):

    def setUp(self):
        self.line_number = 0
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        default_scenario_invoice()

    def test_report_total_by_user(self):
        invoice = get_invoice_time_analysis()
        result = invoice.time_analysis()
        # invoice has a line with no time records
        self.assertIn('', result)
        # fred recorded time on one ticket
        self.assertIn('fred', result)
        fred = result['fred']
        self.assertEqual(1, len(fred))
        self.assertIn(1, fred)
        # sara recorded time on two tickets
        self.assertIn('sara', result)
        sara = result['sara']
        self.assertEqual(2, len(sara))
        self.assertIn(1, sara)
        self.assertIn(3, sara)
        # web user added an invoice line, but didn't record time
        self.assertNotIn('web', result)
        # check net total matches invoice
        net = Decimal()
        for user, tickets in result.items():
            for ticket_pk, totals in tickets.items():
                net = net + totals['net']
        self.assertEqual(invoice.net, net)
