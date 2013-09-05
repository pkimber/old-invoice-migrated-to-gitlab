from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Create demo data for 'invoice'"

    def handle(self, *args, **options):
        print("Created 'invoice' demo data...")
