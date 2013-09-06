from datetime import datetime
from datetime import time

from django.core.management.base import BaseCommand

from crm.models import Ticket
from invoice.tests.model_maker import make_time_record


class Command(BaseCommand):

    help = "Create demo data for 'invoice'"

    def handle(self, *args, **options):
        ticket = Ticket.objects.get(contact__slug='pkimber')
        make_time_record(
            ticket,
            ticket.user,
            'Fence the orchard',
            description="""Please use the posts from the barn.
You can find staples in the wood shed""",
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
        print("Created 'invoice' demo data...")
