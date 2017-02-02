# -*- encoding: utf-8 -*-
import collections

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import WEEKLY, rrule, SU
from decimal import Decimal
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models import Max
from django.utils import timezone
from django.utils.timesince import timeuntil
from reversion import revisions as reversion

from base.model_utils import (
    private_file_store,
    TimedCreateModifyDeleteVersionModel,
    TimeStampedModel,
)
from base.singleton import SingletonModel
from crm.models import Ticket
from finance.models import VatCode
from stock.models import Product


class InvoiceContact(TimeStampedModel):

    contact = models.OneToOneField(settings.CONTACT_MODEL)
    hourly_rate = models.DecimalField(
        blank=True, null=True, max_digits=8, decimal_places=2
    )

    class Meta:
        verbose_name = 'Invoice Contact'
        verbose_name_plural = 'Invoice Contacts'

    def __str__(self):
        result = '{}'.format(self.contact.full_name)
        if self.hourly_rate:
            result = '{} @ {}'.format(result, self.hourly_rate)
        return result

    def get_absolute_url(self):
        return self.contact.get_absolute_url()

reversion.register(InvoiceContact)


class InvoiceError(Exception):

    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr('%s, %s' % (self.__class__.__name__, self.value))


class InvoiceManager(models.Manager):

    def next_number(self):
        qs = self.model.objects.exclude(
            deleted=True,
        ).exclude(
            deleted_version__gt=0,
        )
        result = qs.aggregate(max_id=Max('number'))
        current_number = result.get('max_id') or 0
        return current_number + 1


class Invoice(TimedCreateModifyDeleteVersionModel):
    """
    From Notice 700 The VAT Guide, 16.3.1 General

    VAT invoices must show:
    - an identifying number, which is from a series that is unique and
      sequential;
    - your name, address and VAT registration number;
    - the time of supply (tax point);
    - date of issue (if different to the time of supply);
    - your customer's name (or trading name) and address;
    - a description which identifies the goods or services supplied; and
    - the unit price (see paragraph 16.3.2).

    For each description, you must show the:
    - quantity of goods or extent of the services;
    - charge made, excluding VAT;
    - rate of VAT;
    - total charge made, excluding VAT;
    - rate of any cash discount offered; and
    - total amount of VAT charged, shown in sterling.

    """

    UNIQUE_FIELD_NAME = 'number'

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    invoice_date = models.DateField()
    number = models.IntegerField(default=0)
    # contact = models.ForeignKey(Contact)
    # PJK2
    # new_contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='invoice_contact')
    # PJK3
    # new_contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='invoice_contact')
    # PJK4
    contact = models.ForeignKey(settings.CONTACT_MODEL, related_name='invoice_contact')

    # contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='invoice_contact')
    # crm_contact = models.ForeignKey(Contact)
    # crm_contact = models.ForeignKey(crm_models.Contact) #, related_name='crm_contact_invoice')
    # PJK2
    # contact = models.ForeignKey(settings.CONTACT_MODEL, blank=True, null=True, related_name='invoice_contact')
    pdf = models.FileField(
        upload_to='invoice/%Y/%m/%d', storage=private_file_store, blank=True
    )
    objects = InvoiceManager()

    class Meta:
        ordering = ['pk',]
        unique_together = ('number', 'deleted_version')
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return '{} {}'.format(self.pk, self.invoice_date)

    def get_absolute_url(self):
        return reverse('invoice.detail', args=[self.pk])

    @property
    def can_set_to_draft(self):
        """Can we set this invoice back to a draft state?"""
        result = False
        if not self.is_draft:
            if self.invoice_date == date.today():
                result = True
        return result

    def get_next_line_number(self):
        try:
            self.line_number = self.line_number
        except AttributeError:
            self.line_number = 1
        while(True):
            try:
                self.invoiceline_set.get(line_number=self.line_number)
            except InvoiceLine.DoesNotExist:
                break
            self.line_number = self.line_number + 1
        return self.line_number

    def time_analysis(self):
        """Time analysis by user and ticket for an invoice.

        A dictionary will be returned.  The keys are 'user.username' and
        primary key of the ticket (or zero for invoice lines which do not have
        a time record:

        result = {
            '': {
                0: {'net': Decimal('200'), 'quantity': Decimal('2')}
            },
            'fred': {
                1: {'net': Decimal('1000'), 'quantity': Decimal('10')}
            },
            'sara': {
                1: {'net': Decimal('600'), 'quantity': Decimal('6')},
                3: {'net': Decimal('1400'), 'quantity': Decimal('14')}
            }
        }

        """
        result = {}
        qs = self.invoiceline_set.all()
        for line in qs:
            user_name = ''
            quantity = line.quantity
            if line.has_time_record:
                user_name = line.timerecord.user.username
                # line.quantity does not have sufficient precision
                tx = (datetime.combine(
                        line.timerecord.date_started,
                        line.timerecord.end_time
                    )
                    - datetime.combine(
                        line.timerecord.date_started,
                        line.timerecord.start_time
                    )
                )
                quantity = Decimal((tx.seconds / 3600))
            if not user_name in result:
                result[user_name] = {}
            tickets = result[user_name]
            if line.has_time_record:
                pk = line.timerecord.ticket.pk
                start_date = line.timerecord.date_started
                end_date = line.timerecord.date_started
            else:
                pk = 0
                start_date = line.created
                end_date = line.created
            if not pk in tickets:
                tickets[pk] = dict(
                    start_date=start_date,
                    end_date=end_date,
                    quantity=Decimal(),
                    net=Decimal(),
                )
            totals = tickets[pk]
            if totals['start_date'] > start_date:
                totals['start_date'] = start_date
            if totals['end_date'] < end_date:
                totals['end_date'] = end_date
            totals['net'] = totals['net'] + line.net
            totals['quantity'] = totals['quantity'] + quantity
        return result

    @property
    def description(self):
        if self.is_credit:
            return 'Credit Note'
        else:
            return 'Invoice'

    @property
    def gross(self):
        totals = self.invoiceline_set.aggregate(
            models.Sum('net'), models.Sum('vat')
        )
        return (
            (totals['net__sum'] or Decimal()) +
            (totals['vat__sum'] or Decimal())
        )

    @property
    def has_lines(self):
        return bool(self.invoiceline_set.count())

    @property
    def invoice_number(self):
        return '{:06d}'.format(self.number)

    @property
    def is_credit(self):
        return self.net < Decimal()

    @property
    def is_draft(self):
        return not bool(self.pdf)

    @property
    def net(self):
        totals = self.invoiceline_set.aggregate(models.Sum('net'))
        return totals['net__sum'] or Decimal()

    def remove_time_lines(self):
        if not self.is_draft:
            raise InvoiceError(
                "Time records can only be removed from a draft invoice."
            )
        pks = [i.pk for i in self.invoiceline_set.all()]
        with transaction.atomic():
            for pk in pks:
                line = InvoiceLine.objects.get(pk=pk)
                try:
                    time_record = line.timerecord
                    time_record.invoice_line = None
                    time_record.save()
                    line.delete()
                except TimeRecord.DoesNotExist:
                    pass

    def set_to_draft(self):
        """Set the invoice back to a draft state."""
        if self.can_set_to_draft:
            self.pdf = None
            self.save()
        else:
            raise InvoiceError(
                "You can only set an invoice back to draft "
                "on the day it was created."
            )

    @property
    def vat(self):
        totals = self.invoiceline_set.aggregate(models.Sum('vat'))
        return totals['vat__sum'] or Decimal()

reversion.register(Invoice)


class InvoiceSettingsManager(models.Manager):

    def settings(self):
        try:
            return self.model.objects.get()
        except self.model.DoesNotExist:
            raise InvoiceError(
                "Invoice settings have not been set-up in admin"
            )


class InvoiceSettings(SingletonModel):

    name_and_address = models.TextField()
    phone_number = models.CharField(max_length=100)
    footer = models.TextField()
    time_record_product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        help_text="Product used for time records."
    )
    objects = InvoiceSettingsManager()

    class Meta:
        verbose_name = 'Invoice print settings'

    def __str__(self):
        result = "{}, Phone: {}".format(
            ' '.join(self.name_and_address.split('\n')),
            self.phone_number,
        )
        if self.time_record_product:
            result = '{}, Time record: {}'.format(
                result,
                self.time_record_product.name,
            )
        return result

reversion.register(InvoiceSettings)


class InvoiceLine(TimeStampedModel):
    """
    Invoice line.
    Line numbers for each invoice increment from 1
    Line total can be calculated by adding the net and vat amounts
    """
    invoice = models.ForeignKey(Invoice)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    line_number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, related_name='+')
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    units = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    net = models.DecimalField(max_digits=8, decimal_places=2)
    vat_code = models.ForeignKey(
        VatCode,
        #default=legacy_vat_code,
        related_name='+'
    )
    vat_rate = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        help_text='VAT rate when the line was saved.',
    )
    vat = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ['line_number',]
        verbose_name = 'Invoice line'
        verbose_name_plural = 'Invoice lines'
        unique_together = ('invoice', 'line_number')

    def __str__(self):
        return "{} {} {} @{}".format(
            self.line_number, self.quantity, self.description, self.price
        )

    def clean(self):
        if self.price < Decimal():
            raise ValidationError(
                'Price must always be greater than zero. '
                'To make a credit note, use a negative quantity.'
            )

    def get_absolute_url(self):
        return reverse('invoice.detail', args=[self.invoice.pk])

    def save(self, *args, **kwargs):
        self.vat_rate = self.vat_code.rate
        self.net = self._quantize(self.price * self.quantity)
        self.vat = self._quantize(self.price * self.quantity * self.vat_rate)
        # Call the "real" save() method.
        super().save(*args, **kwargs)

    def _quantize(self, value):
        return value.quantize(Decimal('.01'))

    @property
    def gross(self):
        return self.net + self.vat

    @property
    def is_credit(self):
        return self.quantity < Decimal()

    @property
    def user_can_edit(self):
        return self.invoice.is_draft and not self.has_time_record

    @property
    def has_time_record(self):
        try:
            self.timerecord
            return True
        except TimeRecord.DoesNotExist:
            return False

reversion.register(InvoiceLine)


class InvoiceUser(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    mail_time_summary = models.BooleanField(
        default=False,
        help_text='email a daily summary of time recorded'
    )

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Invoice user'
        verbose_name_plural = 'Invoice user'

    def __str__(self):
        message = ''
        if self.mail_time_summary:
            message = ': mail time summary'
        return '{}{}'.format(self.user.username, message)

reversion.register(InvoiceUser)


class TimeCodeManager(models.Manager):

    def time_codes(self):
        return self.model.objects.exclude(deleted=True)


class TimeCode(TimeStampedModel):

    description = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    objects = TimeCodeManager()

    class Meta:
        ordering = ['description']
        verbose_name = 'Time Code'
        verbose_name_plural = 'Time Codes'

    def __str__(self):
        return self.description


class QuickTimeRecordManager(models.Manager):

    def quick(self, user):
        return self.model.objects.filter(user=user).exclude(deleted=True)


class QuickTimeRecord(TimeStampedModel):
    """Pass this record to ``create_time_record`` to auto-start time."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    time_code = models.ForeignKey(TimeCode)
    chargeable = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)
    objects = QuickTimeRecordManager()

    class Meta:
        ordering = ['-chargeable', 'description']
        verbose_name = 'Quick Time Recording'
        verbose_name_plural = 'Quick Time Recording'

    def __str__(self):
        return self.description


class TimeRecordManager(models.Manager):

    CHARGE = 'Chargeable'
    NON_CHARGE = 'Non-Chargeable'

    def create_time_record(self, ticket, quick_time_record, start_time):
        obj = self.model(
            billable=quick_time_record.chargeable,
            date_started=date.today(),
            start_time=start_time,
            ticket=ticket,
            time_code=quick_time_record.time_code,
            title=quick_time_record.description,
            user=quick_time_record.user,
        )
        obj.save()
        return obj

    def report_charge_non_charge(self, from_date, to_date, user=None):
        """Report of chargeable and non-chargeable time."""
        qs = TimeRecord.objects.filter(
            date_started__gte=from_date,
            date_started__lte=to_date,
        )
        if user:
            qs = qs.filter(user=user)
        result = {}
        for row in qs:
            if row.is_complete:
                if row.billable:
                    if not self.CHARGE in result:
                        result[self.CHARGE] = 0
                    result[self.CHARGE] = result[self.CHARGE] + row.minutes
                else:
                    if not self.NON_CHARGE in result:
                        result[self.NON_CHARGE] = 0
                    result[self.NON_CHARGE] = result[self.NON_CHARGE] + row.minutes
        return result

    def report_time_by_contact(self, from_date, to_date, user=None):
        qs = TimeRecord.objects.filter(
            date_started__gte=from_date,
            date_started__lte=to_date,
        )
        if user:
            qs = qs.filter(user=user)
        result = {}
        for row in qs:
            if row.is_complete:
                slug = row.ticket.contact.slug
                if not slug in result:
                    result[slug] = 0
                result[slug] = result[slug] + row.minutes
        return result

    def report_time_by_ticket(self, user, day):
        """Group time by ticket for a user for a day."""
        qs = TimeRecord.objects.filter(
            user=user,
            date_started=day,
        ).order_by(
            '-start_time',
        )
        result = collections.OrderedDict()
        for row in qs:
            if row.is_complete:
                ticket_pk = row.ticket.pk
                if not ticket_pk in result:
                    result[ticket_pk] = 0
                result[ticket_pk] = result[ticket_pk] + row.minutes
        return result

    def report_time_by_user(self, from_date, to_date):
        qs = TimeRecord.objects.filter(
            date_started__gte=from_date,
            date_started__lte=to_date,
        )
        result = {}
        for row in qs:
            if row.is_complete:
                user_name = row.user.username
                if not user_name in result:
                    result[user_name] = 0
                result[user_name] = result[user_name] + row.minutes
        return result

    def report_time_by_user_by_week_date(self, from_date, to_date, user):
        start_date = from_date + relativedelta(weekday=SU(-1))
        end_date = to_date + relativedelta(weekday=SU(1))
        result = collections.OrderedDict()
        for d in rrule(WEEKLY, dtstart=start_date, until=end_date):
            result[d.date()] = 0
        qs = TimeRecord.objects.filter(
            date_started__gte=from_date,
            date_started__lte=to_date,
            user=user,
        )
        for row in qs:
            if row.is_complete:
                item = row.date_started + relativedelta(weekday=SU(-1))
                result[item] = result[item] + row.minutes
        return result

    def report_time_by_user_by_week(self, from_date, to_date, user):
        data = self.report_time_by_user_by_week_date(from_date, to_date, user)
        result = collections.OrderedDict()
        for key, value in data.items():
            result[key.strftime('%Y_%U')] = value
        return result

    def running(self, user):
        return self.model.objects.filter(user=user, end_time__isnull=True)

    def running_today(self, user):
        return self.running(user).filter(date_started=date.today())

    def start(self, ticket, quick_time_record):
        running = self.running_today(quick_time_record.user)
        count = running.count()
        with transaction.atomic():
            start_time = timezone.localtime(timezone.now()).time()
            if count == 1:
                to_stop = running[0]
                to_stop.stop(start_time)
            elif count > 1:
                raise InvoiceError(
                    "Cannot start a time record when {} are already "
                    "running for '{}'"
                    ".".format(count, quick_time_record.user.username)
                )
            obj = self.create_time_record(
                ticket,
                quick_time_record,
                start_time
            )
        return obj

    def to_invoice(self, contact, iteration_end):
        """
        Find time records:
        - before iteration ended
        - which have not been included on a previous invoice
        - which are chargeable
        """
        return self.model.objects.filter(
            ticket__contact=contact,
            date_started__lte=iteration_end,
            invoice_line__isnull=True,
            billable=True,
        ).order_by(
            'ticket__pk',
            'date_started',
            'start_time',
        )


class TimeRecord(TimeStampedModel):
    """Simple time recording"""

    ticket = models.ForeignKey(Ticket)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_started = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    billable = models.BooleanField(default=False)
    invoice_line = models.OneToOneField(InvoiceLine, blank=True, null=True)
    time_code = models.ForeignKey(TimeCode, blank=True, null=True)
    objects = TimeRecordManager()

    class Meta:
        ordering = ['-date_started', '-start_time']
        verbose_name = 'Time record'
        verbose_name_plural = 'Time records'

    def __str__(self):
        return "Ticket {}, {}: {} from {} to {}".format(
            self.ticket.pk,
            self.title,
            self.date_started,
            self.start_time.strftime('%H:%M:%S') if self.start_time else '',
            self.end_time.strftime('%H:%M:%S') if self.end_time else '',
        )

    def clean(self):
        if (self.start_time and self.end_time
                and self.start_time >= self.end_time):
            raise ValidationError('End time must be after the start time')

    @property
    def deleted(self):
        """No actual delete (yet), so just return 'False'."""
        return False

    def delta(self):
        if self.start_time and self.end_time:
            return self._end_date_time() - self._date_started_time()
        else:
            from datetime import timedelta
            return timedelta()

    def delta_as_string(self):
        if self.start_time and self.end_time:
            return timeuntil(self._end_date_time(), self._date_started_time())
        else:
            return ''

    def get_absolute_url(self):
        return reverse(
            'invoice.time.ticket.list',
            kwargs={'pk': self.ticket.pk}
        )

    def get_summary_description(self):
        return filter(None, (
            self.title,
            self.description,
        ))

    @property
    def is_complete(self):
        """Check the time record is set-up correctly for invoicing."""
        if self.date_started and self.start_time and self.end_time:
            result = True
        else:
            result = False
        return result

    def is_today(self):
        return timezone.now().date() == self.date_started

    def _end_date_time(self):
        return datetime.combine(self.date_started, self.end_time)

    def _has_invoice_line(self):
        """is this time record attached to an invoice"""
        return bool(self.invoice_line)
    has_invoice_line = property(_has_invoice_line)

    @property
    def invoice_quantity(self):
        """
        Convert the time in minutes into hours expressed as a decimal
        e.g. 1 hour, 30 minutes = 1.5.  This figure will be used on invoices.
        """
        return Decimal(self.minutes) / Decimal('60')

    @property
    def minutes(self):
        """ Convert the time difference into minutes """
        td = self.delta()
        return td.days * 1440 + td.seconds / 60

    def stop(self, end_time=None):
        """Stop recording time on this record."""
        if not end_time:
            end_time = timezone.localtime(timezone.now()).time()
        if self.end_time:
            raise InvoiceError(
                "Time record '{}' has already been stopped".format(self.pk)
            )
        self.end_time = end_time
        self.save()

    def _date_started_time(self):
        return datetime.combine(self.date_started, self.start_time)

    def _user_can_edit(self):
        return not self.has_invoice_line
    user_can_edit = property(_user_can_edit)

reversion.register(TimeRecord)
