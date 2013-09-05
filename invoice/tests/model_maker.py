from base.tests.model_maker import clean_and_save

from invoice.models import (
    Invoice,
    InvoiceLine,
    TimeRecord,
)


def make_invoice(invoice_date, contact):
    return clean_and_save(
        Invoice(
            invoice_date=invoice_date,
            contact=contact,
        )
    )


def make_invoice_line(invoice, line_number, quantity, units, price, vat_rate):
    return clean_and_save(
        InvoiceLine(
            invoice=invoice,
            line_number=line_number,
            quantity=quantity,
            units=units,
            price=price,
            vat_rate=vat_rate,
        )
    )


def make_time_record(ticket, user, description, date_started, start_time, end_time, billable):
    return clean_and_save(
        TimeRecord.objects.create(
            ticket=ticket,
            user=user,
            description=description,
            date_started=date_started,
            start_time=start_time,
            end_time=end_time,
            billable=billable
        )
    )
