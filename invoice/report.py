# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal

from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from crm.models import Ticket

from .pdf_utils import MyReport
from .service import InvoiceError


class ReportInvoiceTimeAnalysis(MyReport):

    def report(self, invoice, user, response):
        self._is_valid(invoice, raise_exception=True)
        # Create the document template
        doc = platypus.SimpleDocTemplate(
            response,
            title='Report - Invoice Time Analysis',
            pagesize=A4
        )
        # Container for the 'Flowable' objects
        elements = []
        elements.append(self._head(
            'Time analysis by user and ticket for invoice {}'.format(
                invoice.invoice_number
            )
        ))
        elements.append(platypus.Spacer(1, 12))
        elements.append(self._table_lines(invoice))
        elements.append(self._para(
            'Printed {} by {}'.format(datetime.today(), user.username)
        ))
        doc.build(elements)

    def _get_ticket_description(self, pk):
        if pk:
            ticket = Ticket.objects.get(pk=pk)
            result = '{}, {}'.format(ticket.pk, ticket.title)
        else:
            result = ''
        return result

    def _is_valid(self, invoice, raise_exception=None):
        result = []
        if not invoice.has_lines:
            result.append(
                "Invoice {} has no lines - cannot create "
                "PDF".format(invoice.invoice_number)
            )
        if invoice.is_draft:
            result.append(
                "Invoice {} is a draft invoice - cannot "
                "create the report".format(invoice.invoice_number)
            )
        if result and raise_exception:
            raise InvoiceError(
                ', '.join(result)
            )
        else:
            return result

    def _table_lines(self, invoice):
        """ Create a table for the invoice lines """
        # invoice line header
        data = [[
            self._bold('User'),
            self._bold('Ticket'),
            self._bold('Quantity'),
            self._bold('Net'),
        ]]
        analysis = invoice.time_analysis()
        lines = []
        for user, tickets in analysis.items():
            first_loop = True
            total_net = Decimal()
            total_quantity = Decimal()
            for ticket_pk, totals in tickets.items():
                net = totals['net']
                total_net = total_net + net
                quantity = totals['quantity']
                total_quantity = total_quantity + quantity
                if first_loop:
                    user_name = self._para(user)
                    first_loop = False
                else:
                    user_name = ''
                lines.append([
                    user_name,
                    self._para(self._get_ticket_description(ticket_pk)),
                    quantity,
                    net,
                ])
            lines.append([
                None,
                None,
                self._bold(total_quantity),
                self._bold(total_net),
            ])
        # initial styles
        style = [
            ('GRID', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.gray),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ]
        # column widths
        column_widths = [100, 230, 50, 50]
        # draw the table
        return platypus.Table(
            data + lines,
            colWidths=column_widths,
            repeatRows=1,
            style=style,
        )


import csv
from django.utils import formats

class ReportInvoiceTimeAnalysisCSV(MyReport):

    def report(self, invoice, user, response):
        self._is_valid(invoice, raise_exception=True)
        csv_writer = csv.writer(response, dialect='excel')
        rows = self._produce_csv_rows(invoice)
        for row in rows:
            csv_writer.writerow(row)

    def _get_ticket_description(self, pk):
        if pk:
            ticket = Ticket.objects.get(pk=pk)
            result = ticket.title
        else:
            result = ''
        return result

    def _is_valid(self, invoice, raise_exception=None):
        result = []
        if not invoice.has_lines:
            result.append(
                "Invoice {} has no lines - cannot create "
                "CSV".format(invoice.invoice_number)
            )
        if invoice.is_draft:
            result.append(
                "Invoice {} is a draft invoice - cannot "
                "create the report".format(invoice.invoice_number)
            )
        if result and raise_exception:
            raise InvoiceError(
                ', '.join(result)
            )
        else:
            return result

    def _produce_csv_rows(self, invoice):
        """ Create rows for analysis csv """
        rows = []

        # invoice line header
        rows.append([
            'Invoice Number',
            'Invoice Date',
            'Client Number',
            'Client Name',
            "Client Address",
            "Client Rate",
            'User',
            'Ticket No',
            'Ticket Description',
            'Start Date',
            'End Date',
            'Hours',
            'Net',
        ])

        analysis = invoice.time_analysis()
        for user, tickets in analysis.items():
            total_net = Decimal()
            total_quantity = Decimal()
            for ticket_pk, totals in tickets.items():
                start_date = ""
                end_date = ""
                ticket_title = ""

                if ticket_pk:
                    ticket = Ticket.objects.get(pk=ticket_pk)
                    ticket_title = ticket.title
                    for rec in ticket.timerecord_set.all():
                        if start_date == "" or start_date > rec.date_started:
                            start_date = rec.date_started
                        if end_date == "" or end_date < rec.date_started:
                            end_date = rec.date_started 
                net = totals['net']
                total_net = total_net + net
                quantity = totals['quantity']
                total_quantity = total_quantity + quantity

                rows.append([
                    invoice.invoice_number,
                    invoice.invoice_date,
                    invoice.contact.pk,
                    invoice.contact.name,
                    invoice.contact.address,
                    invoice.contact.hourly_rate,
                    user,
                    ticket_pk,
                    ticket_title,
                    start_date,
                    end_date,
                    quantity,
                    net,
                ])
            rows.append([
                invoice.invoice_number,
                invoice.invoice_date,
                invoice.contact.pk,
                invoice.contact.name,
                invoice.contact.address,
                invoice.contact.hourly_rate,
                user,
                None,
                "Total",
                None,
                None,
                total_quantity,
                total_net,
            ])

        return rows


