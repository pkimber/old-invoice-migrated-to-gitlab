from datetime import datetime
from datetime import time
from decimal import Decimal

from django.test import TestCase

from invoice.models import Invoice
from invoice.service import (
    InvoiceCreateBatch,
    InvoicePrint,
)
from invoice.tests.model_maker import (
    make_invoice_print_settings,
    make_time_record,
)
from login.tests.model_maker import make_user
from crm.tests.model_maker import (
    make_contact,
    make_priority,
    make_ticket,
)


VAT_RATE = Decimal('0.20')


class TestInvoicePrint(TestCase):

    def setUp(self):
        #self.user = make_user('fred')
        #make_config(
        #    make_company(
        #        'Connexion Software Ltd',
        #        'Unit 10, Creedy Centre',
        #        'Crediton',
        #        'Devon',
        #        'EX17 3LQ',
        #        '01363 77 51 71',
        #        make_company_status('Client'),
        #        address_2='117 High Street',
        #    ),
        #    Decimal('20.00')
        #)
        #company = make_company(
        #    'Red House Antiques',
        #    'Upper Street',
        #    'Tavistock',
        #    'Devon',
        #    'PL17 4AB',
        #    '01822 123 456',
        #    make_company_status('Prospect')
        #)
        #project_description = (
        #    'Build a new cloud based customer relationship management system '
        #    'using Open Source software.  Should be able to use the system on '
        #    'a standard browser as well as tablets and modern phones'
        #)
        #project = make_project(
        #    company,
        #    'Customer Relationship Management',
        #    project_description,
        #    iteration_end=timezone.make_aware(datetime(2012, 9, 30), timezone.get_current_timezone()),
        #    hourly_rate=Decimal('300.00')
        #)
        #active = make_task_status(TASK_ACTIVE)
        #to_do = make_task_category('To Do')
        #low = make_task_priority('Low', 1)
        #task = make_task(project, 'Migrate', 'Data migration', to_do, low)
        #make_task_user(task, self.user, active)
        tom = make_user('tom')
        icl = make_contact('icl', 'ICL', hourly_rate=Decimal('20.00'))
        ticket = make_ticket(
            icl,
            tom,
            'Sew',
            'Sewing',
            make_priority('Low', 1),
        )
        make_time_record(
            ticket,
            tom,
            'Make a pillow case',
            datetime(2012, 9, 1),
            time(9, 0),
            time(12, 30),
            True
        )
        make_time_record(
            ticket,
            tom,
            'Buy a new sewing machine',
            datetime(2012, 9, 30),
            time(13, 30),
            time(15, 30),
            True
        )

        ticket_knit = make_ticket(
            icl,
            tom,
            'Knit',
            'Knitting',
            make_priority('Medium', 2),
        )
        #task_backup = make_task(project, 'Backup', 'Backup data', to_do, low)
        #make_task_user(task_backup, self.user, active)
        make_time_record(
            ticket_knit,
            tom,
            'Make a nice cardigan',
            datetime(2012, 9, 1),
            time(10, 10),
            time(12, 30),
            True
        )
        make_invoice_print_settings(
            file_name_prefix='invoice',
            vat_number='',
            name_and_address='Patrick Kimber, Hatherleigh, EX20 3LF',
            phone_number='01234 234 456',
            footer="Please pay by bank transfer<br />For help, please phone<br />Thank you"
        )
        InvoiceCreateBatch(VAT_RATE, datetime(2012, 9, 30)).create()

    def test_invoice_create_pdf(self):
        invoice = Invoice.objects.all()[0]
        InvoicePrint().create_pdf(invoice, None)
