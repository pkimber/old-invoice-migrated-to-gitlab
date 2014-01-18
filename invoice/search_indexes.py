from haystack import indexes

from .models import TimeRecord


class TimeRecordIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return TimeRecord
