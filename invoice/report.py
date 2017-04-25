# -*- encoding: utf-8 -*-
import collections
import csv

from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from django.utils import timezone
from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

from crm.models import Ticket
from report.pdf import MyReport
from report.service import ReportMixin
from .models import TimeRecord
from .service import format_minutes, InvoiceError


def _analysis(analysis):
    return {
        'charge_minutes': analysis[TimeRecord.CHARGE],
        'charge_minutes_format': format_minutes(analysis[TimeRecord.CHARGE]),
        'fixed_minutes': analysis[TimeRecord.FIXED_PRICE],
        'fixed_minutes_format': format_minutes(analysis[TimeRecord.FIXED_PRICE]),
        'non_minutes': analysis[TimeRecord.NON_CHARGE],
        'non_minutes_format': format_minutes(analysis[TimeRecord.NON_CHARGE]),
    }


def time_summary(user, days=None):
    """Time summary for a user.

    """
    if not days:
        days = 4
    # list of the last 10 days
    date_list = []
    d = timezone.now().date()
    for i in range(0, 31):
        date_list.append(d)
        d = d + relativedelta(days=-1)
    # find three days where I worked and display the time summary
    count = 0
    report = collections.OrderedDict()
    for d in date_list:
        data = TimeRecord.objects.report_time_by_ticket(user, d)
        if data:
            summary = {}
            tickets = []
            total_charge = total_fixed = total_non = 0
            for ticket_pk, analysis in data.items():
                ticket = Ticket.objects.get(pk=ticket_pk)
                tickets.append({
                    'pk': ticket.pk,
                    'description': ticket.title,
                    'contact': ticket.contact.get_full_name,
                    'user_name': ticket.contact.user.username,
                    'analysis': _analysis(analysis),
                })
                total_charge = total_charge + analysis[TimeRecord.CHARGE]
                total_fixed = total_fixed + analysis[TimeRecord.FIXED_PRICE]
                total_non = total_non + analysis[TimeRecord.NON_CHARGE]
            total = total_charge + total_fixed + total_non
            summary['tickets'] = tickets
            summary['total'] = total
            summary['total_format'] = format_minutes(total)
            summary['total_charge'] = total_charge
            summary['total_charge_format'] = format_minutes(total_charge)
            summary['total_fixed'] = total_fixed
            summary['total_fixed_format'] = format_minutes(total_fixed)
            summary['total_non'] = total_non
            summary['total_non_format'] = format_minutes(total_non)
            report[d] = summary
            count = count + 1
        # maximum of 5 days
        if count > days:
            break
    return report


def time_summary_by_user(today=None):
    result = {}
    if today is None:
        today = date.today()
    # 12 whole months
    from_date = today + relativedelta(months=-24, day=1)
    to_date = today + relativedelta(day=1, days=-1)
    qs = TimeRecord.objects.filter(
        date_started__gte=from_date,
        date_started__lte=to_date,
    )
    for row in qs:
        if row.is_complete:
            user_name = row.user.username
            if not user_name in result:
                result[user_name] = collections.OrderedDict()
                x = from_date
                while x < to_date:
                    key = x.strftime('%Y-%m')
                    result[user_name][key] = {
                        'label': x.strftime('%b'),
                        'month': x.month,
                        'year': x.year,
                        'charge_minutes': 0,
                        'fixed_minutes': 0,
                        'non_minutes': 0,
                    }
                    x = x + relativedelta(months=+1, day=1)
            key = row.date_started.strftime('%Y-%m')
            data = result[user_name][key]
            minutes = int(row.minutes)
            if row.ticket.fixed_price:
                data['fixed_minutes'] = data['fixed_minutes'] + minutes
            elif row.billable:
                data['charge_minutes'] = data['charge_minutes'] + minutes
            else:
                data['non_minutes'] = data['non_minutes'] + minutes
    return result


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
            'Printed {} by {}'.format(timezone.now(), user.username)
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

    def _format_time(self, user, time_in_hours):
        if not user:
            return "{}".format(time_in_hours)

        seconds = int(float(time_in_hours * 3600) + 0.5)
        hours = seconds // 3600
        minutes = seconds % 3600 // 60
        return "{:0>2}:{:0>2}:{:0>2}".format(hours, minutes, seconds % 60)

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
                    if user:
                        user_name = self._para(user)
                    else:
                        user_name = "Miscellaneous"

                    first_loop = False
                else:
                    user_name = ''

                lines.append([
                    user_name,
                    self._para(self._get_ticket_description(ticket_pk)),
                    self._format_time(user, quantity),
                    net,
                ])

            lines.append([
                None,
                None,
                self._bold(self._format_time(user, total_quantity)),
                self._bold(total_net),
            ])
        # initial styles
        style = [
            ('GRID', (0, 0), (-1, -1), self.GRID_LINE_WIDTH, colors.gray),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ]
        # column widths
        column_widths = [95, 230, 55, 50]
        # draw the table
        return platypus.Table(
            data + lines,
            colWidths=column_widths,
            repeatRows=1,
            style=style,
        )


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
                ticket_title = ""

                if ticket_pk:
                    ticket = Ticket.objects.get(pk=ticket_pk)
                    ticket_title = ticket.title
                net = totals['net']
                total_net = total_net + net
                quantity = totals['quantity']
                total_quantity = total_quantity + quantity

                rows.append([
                    invoice.invoice_number,
                    invoice.invoice_date,
                    invoice.contact.pk,
                    invoice.contact.get_full_name,
                    invoice.contact.hourly_rate,
                    user,
                    ticket_pk,
                    ticket_title,
                    totals['start_date'],
                    totals['end_date'],
                    quantity,
                    net,
                ])
            rows.append([
                invoice.invoice_number,
                invoice.invoice_date,
                invoice.contact.pk,
                invoice.contact.get_full_name,
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


class TimeSummaryByUserReport(ReportMixin):

    def run_csv_report(self, csv_writer):
        csv_writer.writerow((
            'user_name',
            'year',
            'month',
            'label',
            'non_minutes',
            'fixed_minutes',
            'charge_minutes',
        ))
        summary = time_summary_by_user(date.today())
        for user_name, data in summary.items():
            charge_minutes = []
            fixed_minutes = []
            labels = []
            non_minutes = []
            for year_month, values in data.items():
                csv_writer.writerow((
                    user_name,
                    values['year'],
                    values['month'],
                    values['label'],
                    values['non_minutes'],
                    values['fixed_minutes'],
                    values['charge_minutes'],
                ))
        return True


def time_summary_by_user_for_chartist(csv_data):
    result = {}
    count = 0
    first = True
    for row in csv_data:
        if first:
            first = False
        else:
            user_name, year, month, label, non, fix, chg = row
            if user_name not in result:
                count = count + 1
                result[user_name] = {
                    'id': count,
                    'labels': [],
                    'series': [[], [], []],
                }
            result[user_name]['labels'].append(label)
            result[user_name]['series'][0].append(int(chg))
            result[user_name]['series'][1].append(int(fix))
            result[user_name]['series'][2].append(int(non))
    return result
