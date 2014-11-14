# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from celery_haystack.indexes import CelerySearchIndex
from haystack import indexes

from .models import TimeRecord


class TimeRecordIndex(CelerySearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return TimeRecord
