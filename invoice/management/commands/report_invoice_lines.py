# -*- encoding: utf-8 -*-
import csv

from django.core.management.base import BaseCommand
from django.utils import timezone

from invoice.models import Invoice


class Command(BaseCommand):

    help = "Invoice lines (excluding time)"

    def handle(self, *args, **options):
        count = 0
        data = []
        # collections.OrderedDict()
        # user_names = set()
        qs = Invoice.objects.all().order_by('invoice_date', 'created')
        for item in qs:
            # user_names.add(item.user.username)
            # monday = item.date_started + relativedelta(weekday=MO(-1))
            # year_month = (item.date_started.year, item.date_started.month)
            if count % 1000:
                self.stdout.write(item.invoice_date.strftime('%d/%m/%Y'))
                # self.stdout.write(item.date_started.strftime('  {}'.format(year_month)))
            # if not year_month in data:
            #     data[year_month] = {}
            # row = data[year_month]
            # if not item.user.username in row:
            #   row[item.user.username] = 0
            # row[item.user.username] = row[item.user.username] + item.minutes
            for line in item.invoiceline_set.all():
                if not line.has_time_record:
                    data.append([
                        line.invoice.invoice_date.strftime('%d/%m/%Y'),
                        line.invoice.contact.user.username,
                        line.invoice.invoice_number,
                        line.quantity,
                        line.net,
                        line.description,
                        # item.price,
                    ])
            count = count + 1
        # user_names = list(user_names)
        # user_names.sort()
        file_name = 'invoice_lines_{}.csv'.format(
            timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
        )
        with open(file_name, 'w', newline='') as out:
            csv_writer = csv.writer(out, dialect='excel-tab')
            # for user_name in user_names:
            # heading.append(user_name)
            csv_writer.writerow([
                'Date',
                'Contact',
                'Number',
                'Description',
                'Quantity',
                'Net',
                ])

            for row in data:
                csv_writer.writerow(row)
        self.stdout.write("Report written to '{}'...".format(file_name))
