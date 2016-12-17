# -*- encoding: utf-8 -*-
import pytest

from decimal import Decimal

from invoice.service import format_minutes


def test_format_minutes():
    assert '02:00' == format_minutes(120)


def test_format_minutes_2():
    assert '01:15' == format_minutes(75)


def test_format_minutes_3():
    assert '00:15' == format_minutes(15)


def test_format_minutes_decimal():
    assert '00:15' == format_minutes(Decimal(15.3))
