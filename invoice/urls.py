
from django.conf.urls import (
    patterns, url
)

from .views import (
    TimeRecordCreateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^ticket/(?P<pk>\d+)/time/$',
        view=TimeRecordCreateView.as_view(),
        name='invoice.time.create'
        ),
)
