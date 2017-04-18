# -*- encoding: utf-8 -*-
import pytest

from invoice.management.commands import init_app_invoice, report_hours_per_week


@pytest.mark.django_db
def test_init_app():
    """ Test the management command """
    command = init_app_invoice.Command()
    command.handle()


@pytest.mark.django_db
def test_report_hours_per_week():
    """ Test the management command """
    command = report_hours_per_week.Command()
    command.handle()
