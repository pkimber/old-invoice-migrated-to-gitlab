
from django.conf.urls import (
    patterns, url
)

from .views import (
    ContactTimeRecordListView,
    InvoicePreviewListView,
    TicketTimeRecordListView,
    TimeRecordCreateView,
    TimeRecordUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/time/$',
        view=ContactTimeRecordListView.as_view(),
        name='invoice.time.contact.list'
        ),
    url(regex=r'^preview/(?P<slug>[-\w\d]+)/$',
        view=InvoicePreviewListView.as_view(),
        name='invoice.preview'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/time/$',
        view=TicketTimeRecordListView.as_view(),
        name='invoice.time.ticket.list'
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
