from datetime import datetime
from datetime import time

from django.core.management.base import BaseCommand

from crm.models import Ticket
from invoice.tests.model_maker import make_time_record


class Command(BaseCommand):

    help = "Create demo data for 'invoice'"

    def handle(self, *args, **options):
        tickets = Ticket.objects.filter(contact__slug='pkimber')
        if not len(tickets) > 1:
            raise Exception(
                "Expected 'crm' demo data to create two tickets "
                "for contact '{}'".format('pkimber')
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
        print("Created 'invoice' demo data...")
