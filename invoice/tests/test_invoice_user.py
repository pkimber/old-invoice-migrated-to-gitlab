# -*- encoding: utf-8 -*-
import pytest

from invoice.tests.factories import InvoiceUserFactory
from login.tests.factories import UserFactory


@pytest.mark.django_db
def test_factory():
    InvoiceUserFactory()


@pytest.mark.django_db
def test_str():
    obj = InvoiceUserFactory(
        user=UserFactory(username='pat'),
        mail_time_summary=False,
    )
    assert 'pat' == str(obj)


@pytest.mark.django_db
def test_str_email_time_summary():
    obj = InvoiceUserFactory(
        user=UserFactory(username='pat'),
        mail_time_summary=True,
    )
    assert 'pat: mail time summary' == str(obj)
