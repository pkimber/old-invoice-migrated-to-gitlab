# -*- encoding: utf-8 -*-
"""
Test time records.
"""
from django.test import TestCase

from crm.tests.scenario import default_scenario_crm
from invoice.tests.factories import (
    InvoiceFactory,
    InvoiceLineFactory,
    InvoiceSettingsFactory,
    TimeRecordFactory,
)
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)
from search.tests.helper import check_search_methods


class TestTimeRecord(TestCase):

    #def setUp(self):
    #    default_scenario_login()
    #    user_contractor()
    #    default_scenario_crm()
    #    default_scenario_invoice()

    def test_search_methods(self):
        #time_record = get_timerecord_fence_dig_holes()
        time_record = TimeRecordFactory()
        check_search_methods(time_record)

    def test_str(self):
        #time_record = get_timerecord_fence_dig_holes()
        time_record = TimeRecordFactory()
        str(time_record)

    def test_user_can_edit(self):
        #time_record = get_timerecord_fence_dig_holes()
        time_record = TimeRecordFactory()
        self.assertTrue(time_record.user_can_edit)

    def test_user_can_edit_invoice_line(self):
        #time_record = get_timerecord_paperwork_template()
        invoice_line = InvoiceLineFactory()
        time_record = TimeRecordFactory(invoice_line=invoice_line)
        #time_record = TimeRecordFactory()
        self.assertFalse(time_record.user_can_edit)
