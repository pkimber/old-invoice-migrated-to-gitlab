# -*- encoding: utf-8 -*-
from django.test import TestCase

from invoice.management.commands import init_app_invoice


class TestCommand(TestCase):

    def test_init_app(self):
        """ Test the management command """
        command = init_app_invoice.Command()
        command.handle()
