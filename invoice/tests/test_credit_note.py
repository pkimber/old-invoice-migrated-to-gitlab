# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .factories import InvoiceFactory


class TestCreditNote(TestCase):

    def test_factory(self):
        """ Create a simple credit note."""
        invoice = InvoiceFactory()
