from django.test import TestCase

from crm.management.commands import demo_data_crm
from invoice.management.commands import demo_data_invoice
from invoice.management.commands import init_app_invoice
from login.management.commands import demo_data_login


class TestCommand(TestCase):

    def test_demo_data(self):
        """ Test the management command """
        demo_data_login.Command().handle()
        demo_data_crm.Command().handle()
        demo_data_invoice.Command().handle()

    def test_init_app(self):
        """ Test the management command """
        command = init_app_invoice.Command()
        command.handle()
