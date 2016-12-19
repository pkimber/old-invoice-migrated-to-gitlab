# -*- encoding: utf-8 -*-
import logging

from celery import shared_task
from django.utils import timezone

from invoice.models import InvoiceUser
from mail.service import queue_mail_message
from mail.tasks import process_mail
from .report import time_summary


logger = logging.getLogger(__name__)


@shared_task
def mail_time_summary():
    users = []
    for item in InvoiceUser.objects.all():
        if item.mail_time_summary and item.user.email:
            users.append(item.user)
    for user in users:
        logger.info('mail_time_summary: {}'.format(user.username))
        report = time_summary(user, days=1)
        message = '<table border="0">'
        for d, summary in report.items():
            message = message + '<tr colspan="3">'
            message = message + '<td>{}</td>'.format(d.strftime('%d/%m/%Y %A'))
            message = message + '</tr>'
            for ticket in summary['tickets']:
                message = message + '<tr>'
                message = message + '<td>{}</td>'.format(ticket['pk'])
                message = message + '<td>{}, {}</td>'.format(
                    ticket['contact'],
                    ticket['description'],
                )
                message = message + '<td>{}</td>'.format(
                    ticket['format_minutes'],
                )
                message = message + '</tr>'
            message = message + '<tr>'
            message = message + '<td></td><td></td>'
            message = message + '<td><b>{}</b></td>'.format(
                summary['format_total']
            )
            message = message + '</tr>'
        message = message + '</table>'
        queue_mail_message(
            user,
            [user.email],
            'Time Summary for {}'.format(timezone.now().strftime('%d/%m/%Y')),
            message,
        )
    if users:
        process_mail.delay()
