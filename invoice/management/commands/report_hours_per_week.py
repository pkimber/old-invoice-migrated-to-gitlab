# -*- encoding: utf-8 -*-
import collections
import csv
import os

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from invoice.models import TimeRecord


class Command(BaseCommand):

    help = "Time by User by Week for the Last Year"

    def handle(self, *args, **options):
        file_name = 'report_time_by_user_by_week_date.csv'
        if os.path.exists(file_name):
            raise CommandError("'{}' already exists.".format(file_name))
        to_date = timezone.now()
        from_date = to_date + relativedelta(years=-1)
        user_qs = get_user_model().objects.filter(is_staff=True)
        users_list = [user for user in user_qs]
        result = collections.OrderedDict()
        for user in users_list:
            data = TimeRecord.objects.report_time_by_user_by_week_date(
                from_date,
                to_date,
                user,
            )
            for key, value in data.items():
                if not key in result:
                    result[key] = []
                result[key].append(int(value))
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(
                csv_file,
                dialect='excel-tab',
            )
            csv_writer.writerow(['Date'] + users_list)
            for key, value in result.items():
                csv_writer.writerow([key] + value)
        self.stdout.write("Report - created...")
