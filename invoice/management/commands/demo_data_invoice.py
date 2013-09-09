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
from login.tests.scenario import (
    get_user_fred,
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
            farm = get_contact_farm()
        except Contact.DoesNotExist:
            raise Exception(
                "Expected 'crm' demo data to create a contact"
                "with the slug value of '{}'".format('fred')
            )
        self._invoice_settings()
        self._time_for_ticket(farm)
        self._invoice_for_contact(farm)
        print("Created 'invoice' demo data...")

    def _invoice_for_contact(self, farm):
        tickets = farm.ticket_set.all()
        if not len(tickets) > 0:
            raise Exception(
                "Expected 'crm' demo data to have created a ticket "
                "for contact '{}'".format('fred')
            )
        ticket = tickets[0]
        make_time_record(
            ticket,
            ticket.user,
            'Make a pillow case',
            datetime(2012, 9, 1),
            time(9, 0),
            time(12, 30),
            True,
        )
        # time record is on the day of the iteration end date
        make_time_record(
            ticket,
            ticket.user,
            'Buy a new sewing machine',
            datetime(2012, 9, 30),
            time(13, 30),
            time(15, 30),
            True,
        )
        invoice_create = InvoiceCreate(datetime(2013, 9, 6))
        invoice_create.create(farm)

    def _invoice_settings(self):
        make_invoice_settings(
            vat_rate=Decimal('0.20'),
            vat_number='',
            name_and_address='Patrick Kimber\nHatherleigh\nEX20 1AB',
            phone_number='01234 234 456',
            footer="Please pay by bank transfer\nThank you"
        )

    def _time_for_ticket(self, fred):
        tickets = Ticket.objects.filter(contact=fred)
        if not len(tickets) > 1:
            raise Exception(
                "Expected 'crm' demo data to create two tickets "
                "for contact '{}'".format(fred.username)
            )
        description = """Please use the posts from the barn.
You can find staples in the wood shed"""
        ticket = tickets[0]
        make_time_record(
            ticket,
            ticket.user,
            'Fence the orchard',
            description=description,
            date_started=datetime(2012, 11, 13),
            start_time=time(9, 0),
            end_time=time(9, 30),
            billable=True,
        )
        make_time_record(
            ticket,
            ticket.user,
            'Feed the chickens',
            date_started=datetime(2012, 11, 14),
            start_time=time(12, 0),
            end_time=time(12, 45),
            billable=True,
        )
        ticket = tickets[1]
        make_time_record(
            ticket,
            ticket.user,
            'Milk the cows',
            date_started=datetime(2012, 11, 13),
            start_time=time(5, 0),
            end_time=time(8, 30),
            billable=True,
        )
