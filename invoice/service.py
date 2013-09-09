import os

from datetime import datetime
from decimal import Decimal
from StringIO import StringIO

from django.core.files.base import ContentFile

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet

from crm.models import Contact
from invoice.models import (
    Invoice,
    InvoiceLine,
    InvoiceSettings,
    TimeRecord,
)


class InvoiceError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class InvoiceCreate(object):
    """ Create invoices for outstanding time records """

    def __init__(self, iteration_end):
        self.iteration_end = iteration_end

    def create(self, contact):
        """ Create invoices from time records """
        self.is_valid(contact, raise_exception=True)
        invoice = None
        line_number = 0
        print_settings = self._get_print_settings()
        time_records = self._get_time_records(contact, self.iteration_end)
        for time_record in time_records:
            if not invoice:
                invoice = Invoice(
                    invoice_date=datetime.today(),
                    contact=contact,
                )
                invoice.save()
            line_number = line_number + 1
            invoice_line = InvoiceLine(
                invoice=invoice,
                line_number=line_number,
                quantity=time_record.invoice_quantity,
                price=contact.hourly_rate,
                units='hours',
                vat_rate=print_settings.vat_rate
            )
            invoice_line.save()
            # link time record to invoice line
            time_record.invoice_line = invoice_line
            time_record.save()
        if invoice:
            invoice.save()
        return invoice

    def draft(self, contact):
        """Return a queryset with time records selected to invoice"""
        return self._get_time_records(contact, self.iteration_end)

    def is_valid(self, contact, raise_exception=None):
        result = []
        try:
            InvoiceSettings.objects.get()
        except InvoiceSettings.DoesNotExist:
            result.append(
                'Invoice print settings have not been set-up in admin'
            )
        if not contact.hourly_rate:
            result.append(
                'Cannot create invoice - no hourly rate for the contact'
            )
        if result and raise_exception:
            raise InvoiceError(
                ', '.join(result)
            )
        else:
            return result

    def _get_print_settings(self):
        try:
            return InvoiceSettings.objects.get()
        except InvoiceSettings.DoesNotExist:
            raise InvoiceError(
                "invoice print settings have not been set-up in admin"
            )

    def _get_time_records(self, contact, iteration_end):
        """
        Find time records:
        - before iteration ended
        - which have not been included on a previous invoice
        - which are billable
        """
        return TimeRecord.objects.filter(
            ticket__contact=contact,
            date_started__lte=iteration_end,
            invoice_line__isnull=True,
            billable=True,
        ).order_by(
            'ticket__pk',
            'date_started',
        )


class InvoiceCreateBatch(object):

    def __init__(self, iteration_end):
        self.iteration_end = iteration_end

    def create(self):
        """ Create invoices from time records """
        invoice_create = InvoiceCreate(self.iteration_end)
        for contact in Contact.objects.all():
            invoice_create.create(contact)


class InvoicePrint(object):
    """
    Write a PDF for an invoice which has already been created in the database.
    """

    def __init__(self):
        # Use the sample style sheet.
        style_sheet = getSampleStyleSheet()
        self.body = style_sheet["BodyText"]
        self.head_1 = style_sheet["Heading1"]
        self.head_2 = style_sheet["Heading2"]
        self.GRID_LINE_WIDTH = 0.25

    def _para(self, text):
        return platypus.Paragraph(text, self.body)

    def _bold(self, text):
        return self._para('<b>{}</b>'.format(text))

    def _head(self, text):
        return platypus.Paragraph(text, self.head_2)

    def _image(self, file_name):
        return platypus.Image(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'static',
            file_name
        ))

    def _get_column_styles(self, column_widths):
        # style - add vertical grid lines
        style = []
        for idx in range(len(column_widths) - 1):
            style.append((
                'LINEAFTER',
                (idx, 0),
                (idx, -1),
                self.GRID_LINE_WIDTH,
                colors.gray)
            )
        return style

    def _get_print_settings(self):
        try:
            return InvoiceSettings.objects.get()
        except InvoiceSettings.DoesNotExist:
            raise InvoiceError(
                "invoice print settings have not been set-up in admin"
            )

    def create_pdf(self, invoice, header_image):
        # Create the document template
        buff = StringIO()
        doc = platypus.SimpleDocTemplate(
            buff,
            title='Invoice',
            pagesize=A4
        )
        print_settings = self._get_print_settings()
        # Container for the 'Flowable' objects
        elements = []
        elements.append(
            self._table_header(invoice, print_settings, header_image)
        )
        elements.append(platypus.Spacer(1, 12))
        elements.append(self._table_lines(invoice))
        elements.append(self._table_totals(invoice))
        for text in self._text_footer(print_settings.footer):
            elements.append(self._para(text))
        # write the document to disk
        doc.build(elements)
        pdf = buff.getvalue()
        buff.close()
        invoice_filename = '{}-{}.pdf'.format(
            print_settings.file_name_prefix, invoice.invoice_number
        )
        invoice.pdf.save(invoice_filename, ContentFile(pdf))
        return invoice_filename

    def _table_invoice_detail(self, invoice):
        """
        Create a (mini) table containing the invoice date and number.

        This is returned as a 'mini table' which is inserted into the main
        header table to keep headings and data aligned.
        """
        # invoice header
        invoice_header_data = [
            [
                self._bold('Date'),
                '%s' % invoice.invoice_date.strftime('%d/%m/%Y')
            ],
            [
                self._bold('Invoice'),
                '%s' % invoice.invoice_number
            ],
        ]
        return platypus.Table(
            invoice_header_data,
            colWidths=[70, 200],
            style=[
                #('GRID', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ]
        )

    def _table_header(self, invoice, print_settings, header_image):
        """
        Create a table for the top section of the invoice (before the project
        description and invoice detail)
        """
        left = []
        right = []

        # left hand content
        left.append(self._para(self._text_invoice_address(invoice)))
        left.append(platypus.Spacer(1, 12))
        left.append(self._table_invoice_detail(invoice))

        # right hand content
        if header_image:
            right.append(self._image(header_image))
        right.append(self._para(
            self._text_our_address(print_settings.name_and_address)
        ))
        right.append(self._bold(print_settings.phone_number))
        if print_settings.vat_number:
            right.append(self._para(
                self._text_our_vat_number(print_settings.vat_number)
            ))

        heading = [platypus.Paragraph('Invoice', self.head_1)]

        # If the invoice has a logo, then the layout is different
        if header_image:
            data = [
                [
                    heading + left,     # left
                    right,              # right
                ],
            ]
        else:
            data = [
                [
                    heading,            # left (row one)
                    [],                 # right (row one)
                ],
                [
                    left,               # left (row two)
                    right,              # right (row two)
                ],
            ]

        return platypus.Table(
            data,
            colWidths=[300, 140],
            style=[
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                #('GRID', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.grey),
            ]
        )

    def _table_lines(self, invoice):
        """ Create a table for the invoice lines """
        # invoice line header
        data = [[
            None,
            self._para('Description'),
            'Net',
            '%VAT',
            'VAT',
            'Gross',
        ]]
        # lines
        lines = self._get_invoice_lines(invoice)
        # initial styles
        style = [
            #('BOX', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.gray),
            ('LINEABOVE', (0, 0), (-1, 0), self.GRID_LINE_WIDTH, colors.gray),
            ('VALIGN', (0, 0), (0, -1), 'TOP'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ]
        # style - add horizontal grid lines
        for idx, line in enumerate(lines):
            row_number = line[0]
            if not row_number:
                style.append((
                    'LINEBELOW',
                    (0, idx),
                    (-1, idx),
                    self.GRID_LINE_WIDTH,
                    colors.gray)
                )
        # column widths
        column_widths = [20, 230, 50, 40, 50, 50]
        style = style + self._get_column_styles(column_widths)
        # draw the table
        return platypus.Table(
            data + lines,
            colWidths=column_widths,
            repeatRows=1,
            style=style,
        )

    def _table_totals(self, invoice):
        """ Create a table for the invoice totals """
        gross = invoice.gross
        net = invoice.net
        vat = invoice.gross - invoice.net
        data = [[
            self._bold('Totals'),
            '%.2f' % net,
            None,
            '%.2f' % vat,
            '%.2f' % gross,
        ]]
        style = [
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('LINEBELOW', (0, 0), (-1, 0), self.GRID_LINE_WIDTH, colors.gray),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ]
        column_widths = [250, 50, 40, 50, 50]
        style = style + self._get_column_styles(column_widths)
        return platypus.Table(
            data,
            colWidths=column_widths,
            style=style,
        )

    def _get_invoice_line_description(self, invoice_line):
        result = []
        if invoice_line.description:
            result.append('{}'.format(invoice_line.description))
        if invoice_line.has_time_record:
            time_record = invoice_line.timerecord
            if time_record.description:
                result.append('{}'.format(time_record.description))
            result.append('%s %s to %s' % (
                time_record.date_started.strftime("%a %d %b %Y"),
                time_record.start_time.strftime("from %H:%M"),
                time_record.end_time.strftime("%H:%M"),
            ))
        result.append('%.2f %s @ %s pounds' % (
            invoice_line.quantity,
            invoice_line.units,
            invoice_line.price
        ))
        return '<br />'.join(result)

    def _get_invoice_lines(self, invoice):
        data = []
        ticket_pk = None
        for line in invoice.invoiceline_set.all():
            # ticket heading (do not repeat)
            if line.has_time_record and ticket_pk != line.timerecord.ticket.pk:
                ticket_pk = line.timerecord.ticket.pk
                data.append([
                    None,
                    self._bold(line.timerecord.ticket.title),
                    None,
                    None,
                    None,
                    None,
                ])
            data.append([
                '%s' % line.line_number,
                self._para(self._get_invoice_line_description(line)),
                '%.2f' % line.net,
                '{:g}'.format(self._round(line.vat_rate * Decimal('100'))),
                '%.2f' % line.vat,
                '%.2f' % (line.vat + line.net),
            ])
        return data

    def _round(self, value):
        return value.quantize(Decimal('.01'))

    def _text_footer(self, footer):
        """ Build a list of text to go in the footer """
        result = []
        result.append('All prices in pounds sterling')
        lines = footer.split('\n')
        for text in lines:
            result.append(text)
        return tuple(result)

    def _text_invoice_address(self, invoice):
        """ Name and address of contact we are invoicing """
        lines = [invoice.contact.name]
        lines = lines + invoice.contact.address.split('\n')
        return '<br />'.join(lines)

    def _text_our_address(self, name_and_address):
        """ Company name and address """
        lines = name_and_address.split(',')
        return '<br />'.join(lines)

    def _text_our_vat_number(self, vat_number):
        return '<b>VAT Number</b> {}'.format(vat_number)
