"""
Test time records.
"""
from django.test import TestCase

from crm.tests.scenario import default_scenario_crm
from invoice.tests.scenario import (
    get_timerecord_fence_dig_holes,
    get_timerecord_paperwork_template,
    time_fencing,
    time_paperwork,
)
from login.tests.scenario import (
    default_scenario_login,
    user_contractor,
)
from search.tests.helper import check_search_methods


class TestTimeRecord(TestCase):

    def setUp(self):
        default_scenario_login()
        user_contractor()
        default_scenario_crm()
        time_fencing()
        time_paperwork()

    def test_search_methods(self):
        time_record = get_timerecord_fence_dig_holes()
        check_search_methods(time_record)

    def test_str(self):
        time_record = get_timerecord_fence_dig_holes()
        str(time_record)

    def test_user_can_edit(self):
        time_record = get_timerecord_fence_dig_holes()
        self.assertTrue(time_record.user_can_edit)

    def test_user_can_edit_invoice_line(self):
        time_record = get_timerecord_paperwork_template()
        self.assertFalse(time_record.user_can_edit)
