# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from datetime import time
from decimal import Decimal

from django.core.management.base import BaseCommand

from crm.models import Contact
from crm.tests.scenario import get_contact_farm
from invoice.tests.scenario import default_scenario_invoice


class Command(BaseCommand):

    help = "Create demo data for 'invoice'"

    def handle(self, *args, **options):
        try:
            get_contact_farm()
        except Contact.DoesNotExist:
            raise Exception(
                "Expected to find 'crm' demo data before "
                "adding 'invoice' demo data."
            )
        default_scenario_invoice()
        print("Created 'invoice' demo data...")
