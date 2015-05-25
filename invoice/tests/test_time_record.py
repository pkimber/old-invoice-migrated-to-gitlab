# -*- encoding: utf-8 -*-
"""
Test time records.
"""
from django.test import TestCase

from invoice.tests.factories import (
    InvoiceLineFactory,
    TimeRecordFactory,
)
from search.tests.helper import check_search_methods


class TestTimeRecord(TestCase):

    def test_search_methods(self):
        time_record = TimeRecordFactory()
        check_search_methods(time_record)

    def test_str(self):
        time_record = TimeRecordFactory()
        str(time_record)

    def test_user_can_edit(self):
        time_record = TimeRecordFactory()
        self.assertTrue(time_record.user_can_edit)

    def test_user_can_edit_invoice_line(self):
        invoice_line = InvoiceLineFactory()
        time_record = TimeRecordFactory(invoice_line=invoice_line)
        self.assertFalse(time_record.user_can_edit)
