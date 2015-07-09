# -*- encoding: utf-8 -*-
import csv
import os

from django.core.management.base import BaseCommand

from invoice.models import TimeRecord


class Command(BaseCommand):

    help = "Export ticket time to a CSV file"
    
    def _jobs_board_tickets(self):
        return (
            732,
            746,
            747,
            748,
            749,
            750,
            751,
            752,
            753,
            754,
            755,
            756,
            757,
            758,
            759,
            906,
            976,
        )
    
    def _payment_plan_tickets(self):
        return (
            644,
        )
    
    def handle(self, *args, **options):
        """Export ticket time to a CSV file.

        Columns:

        - ticket number
        - user name
        - billable - True or False
        - date started
        - minutes

        """
        tickets = self._jobs_board_tickets()
        # tickets = self._payment_plan_tickets()
        tickets = list(tickets)
        tickets.sort()
        file_name = '{}_ticket_time.csv'.format(
            '_'.join([str(i) for i in tickets])
        )
        if os.path.exists(file_name):
            raise Exception(
                "Export file, '{}', already exists.  "
                "Cannot export time.".format(file_name)
            )
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, dialect='excel-tab')
            for tr in TimeRecord.objects.filter(ticket__pk__in=tickets):
                csv_writer.writerow([
                    tr.ticket.pk,
                    tr.user.username,
                    tr.billable,
                    tr.has_invoice_line,
                    tr.date_started,
                    tr._timedelta_minutes(),
                ])
        print("Exported time to {}".format(file_name))
