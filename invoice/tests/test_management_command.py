# -*- encoding: utf-8 -*-
from django.test import TestCase

from crm.management.commands import demo_data_crm
from invoice.management.commands import init_app_invoice
from login.management.commands import demo_data_login


class TestCommand(TestCase):

    def test_init_app(self):
        """ Test the management command """
        command = init_app_invoice.Command()
        command.handle()
