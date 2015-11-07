# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from invoice.service import report


class Command(BaseCommand):

    help = "Update report data"

    def handle(self, *args, **options):
        report()
        self.stdout.write("Report data - updated...")
