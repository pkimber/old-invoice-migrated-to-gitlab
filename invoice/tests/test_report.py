"""
Test invoice manager.
"""
from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from crm.tests.scenario import (
    default_scenario_crm,
    get_contact_farm,
)
from login.tests.scenario import (
    default_scenario_login,
    get_user_fred,
    get_user_sara,
    get_user_staff,
    user_contractor,
)

from invoice.models import Invoice
from invoice.tests.model_maker import (
    make_invoice,
    make_invoice_line,
)
from invoice.tests.scenario import (
    invoice_settings,
    time_paperwork,
)


class TestReport(TestCase):

    def setUp(self):
        user_contractor()
        default_scenario_login()
        default_scenario_crm()
        invoice_settings()
        self.invoice = time_paperwork()
        make_invoice_line(
            self.invoice, 3, 2.0, 'hours', 100.00, 0.00, user=get_user_fred()
        )
        make_invoice_line(
            self.invoice, 4, 8.0, 'hours', 100.00, 0.00, user=get_user_fred()
        )
        make_invoice_line(
            self.invoice, 5, 6.0, 'hours', 100.00, 0.00, user=get_user_sara()
        )
        make_invoice_line(
            self.invoice, 6, 14.0, 'hours', 100.00, 0.00, user=get_user_sara()
        )

    def test_report_total_by_user(self):
        result = self.invoice.time_analysis()
        self.assertIn('fred', result)
        self.assertIn('sara', result)
        self.assertIn('staff', result)
        net = Decimal()
        for user, tickets in result.items():
            for ticket_pk, totals in tickets.items():
                net = net + totals['net']
        self.assertEqual(self.invoice.net, net)
