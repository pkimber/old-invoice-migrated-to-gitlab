from datetime import datetime
from datetime import time
from decimal import Decimal

from django.core.management.base import BaseCommand

from crm.models import (
    Contact,
    Ticket,
)
from crm.tests.scenario import (
    get_contact_farm,
)
from invoice.tests.scenario import (
    invoice_settings,
    time_fencing,
    time_paperwork,
)
from invoice.service import (
    InvoiceCreate,
)
from invoice.tests.model_maker import (
    make_invoice_settings,
    make_time_record,
)


class Command(BaseCommand):

    help = "Create demo data for 'invoice'"

    def handle(self, *args, **options):
        try:
            get_contact_farm()
        except Contact.DoesNotExist:
            raise Exception(
                "Expected 'crm' demo data to create a contact"
            )
        invoice_settings()
        time_fencing()
        time_paperwork()
        print("Created 'invoice' demo data...")
