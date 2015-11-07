# -*- encoding: utf-8 -*-
import pytest

from invoice.management.commands import (
    init_app_invoice,
    report_invoice,
)


@pytest.mark.django_db
def test_init_app():
    """ Test the management command """
    command = init_app_invoice.Command()
    command.handle()


@pytest.mark.django_db
def test_report_invoice():
    """ Test the management command """
    command = report_invoice.Command()
    command.handle()
