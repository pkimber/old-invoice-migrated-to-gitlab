from datetime import datetime

from crm.models import Contact
from invoice.models import (
    Invoice,
    InvoiceLine,
)


class CrmInvoiceError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class InvoiceCreate(object):
    """ Create invoices for outstanding time records """

    def __init__(self, vat_rate, iteration_end):
        self.iteration_end = iteration_end
        self.vat_rate = vat_rate

    def create(self, contact):
        """ Create invoices from time records """
        self._check_contact_data(contact)
        invoice = None
        line_number = 0
        for ticket in contact.ticket_set.all():
            ticket_time_records = self._get_time_records_for_ticket(
                ticket, self.iteration_end
            )
            for time_record in ticket_time_records:
                if not invoice:
                    invoice = Invoice(
                        invoice_date=datetime.today(),
                        contact=contact,
                    )
                    invoice.save()
                hourly_rate = self._get_hourly_rate(ticket)
                line_number = line_number + 1
                invoice_line = InvoiceLine(
                    invoice=invoice,
                    line_number=line_number,
                    quantity=time_record.invoice_quantity,
                    price=hourly_rate,
                    units='hours',
                    vat_rate=self.vat_rate
                )
                invoice_line.save()
                # link time record to invoice line
                time_record.invoice_line = invoice_line
                time_record.save()
        if invoice:
            invoice.save()
        return invoice

    def _check_contact_data(self, contact):
        if not contact.hourly_rate:
            raise CrmInvoiceError(
                'Hourly rate for the contact has not been set'
            )

    def _get_hourly_rate(self, ticket):
        return ticket.contact.hourly_rate

    def _get_time_records_for_ticket(self, ticket, iteration_end):
        """
        Find time records:
        - before iteration ended
        - which have not been included on a previous invoice
        - which are billable
        """
        return ticket.timerecord_set.filter(
            date_started__lte=iteration_end,
            invoice_line__isnull=True,
            billable=True
        )


class InvoiceCreateBatch(object):

    def __init__(self, vat_rate, iteration_end):
        self.iteration_end = iteration_end
        self.vat_rate = vat_rate

    def create(self):
        """ Create invoices from time records """
        invoice_create = InvoiceCreate(self.vat_rate, self.iteration_end)
        for contact in Contact.objects.all():
            invoice_create.create(contact)
