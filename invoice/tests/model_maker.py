from base.tests.model_maker import clean_and_save

from invoice.models import (
    Invoice,
    InvoiceLine,
    InvoicePrintSettings,
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


def make_invoice_print_settings(file_name_prefix, vat_number, name_and_address, phone_number, footer):
    return clean_and_save(
        InvoicePrintSettings(
            file_name_prefix=file_name_prefix,
            vat_number=vat_number,
            name_and_address=name_and_address,
            phone_number=phone_number,
            footer=footer,
        )
    )


def make_time_record(ticket, user, name, date_started, start_time, end_time, billable, **kwargs):
    return clean_and_save(
        TimeRecord.objects.create(
            ticket=ticket,
            user=user,
            name=name,
            date_started=date_started,
            start_time=start_time,
            end_time=end_time,
            billable=billable,
            **kwargs
        )
    )
