
from django.conf.urls import (
    patterns, url
)

from .views import (
    TimeRecordCreateView,
    TimeRecordListView,
    TimeRecordUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^ticket/(?P<pk>\d+)/time/$',
        view=TimeRecordListView.as_view(),
        name='invoice.time.list'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/time/add/$',
        view=TimeRecordCreateView.as_view(),
        name='invoice.time.create'
        ),
    url(regex=r'^time/(?P<pk>\d+)/edit/$',
        view=TimeRecordUpdateView.as_view(),
        name='invoice.time.update'
        ),
)
