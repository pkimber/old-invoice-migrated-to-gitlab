from base.tests.model_maker import clean_and_save

from invoice.models import (
    Invoice,
    InvoiceLine,
    InvoiceSettings,
    TimeRecord,
)


def make_invoice(user, invoice_date, contact):
    return clean_and_save(
        Invoice(
            user=user,
            invoice_date=invoice_date,
            contact=contact,
        )
    )


def make_invoice_line(
        invoice, line_number, quantity, units, price, vat_rate, **kwargs):
    defaults = dict(
        user=invoice.user,
        invoice=invoice,
        line_number=line_number,
        quantity=quantity,
        units=units,
        price=price,
        vat_rate=vat_rate,
    )
    defaults.update(kwargs)
    return clean_and_save(InvoiceLine(**defaults))


def make_invoice_settings(
        vat_rate, vat_number,
        name_and_address, phone_number,
        footer):
    return clean_and_save(
        InvoiceSettings(
            vat_rate=vat_rate,
            vat_number=vat_number,
            name_and_address=name_and_address,
            phone_number=phone_number,
            footer=footer,
        )
    )


def make_time_record(
        ticket, user, title, date_started,
        start_time, end_time, billable, **kwargs):
    return clean_and_save(
        TimeRecord.objects.create(
            ticket=ticket,
            user=user,
            title=title,
            date_started=date_started,
            start_time=start_time,
            end_time=end_time,
            billable=billable,
            **kwargs
        )
    )
