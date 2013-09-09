
from django.conf.urls import (
    patterns, url
)

from .views import (
    ContactTimeRecordListView,
    invoice_download,
    InvoiceCreateView,
    InvoiceListView,
    TicketTimeRecordListView,
    TimeRecordCreateView,
    TimeRecordListView,
    TimeRecordUpdateView,
)


urlpatterns = patterns(
    '',
    url(regex=r'^contact/(?P<slug>[-\w\d]+)/time/$',
        view=ContactTimeRecordListView.as_view(),
        name='invoice.time.contact.list'
        ),
    url(regex=r'^create/(?P<slug>[-\w\d]+)/$',
        view=InvoiceCreateView.as_view(),
        name='invoice.create'
        ),
    url(regex=r'^$',
        view=InvoiceListView.as_view(),
        name='invoice.list'
        ),
    url(regex=r'^download/(?P<pk>\d+)/$',
        view=invoice_download,
        name='invoice.download'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/time/$',
        view=TicketTimeRecordListView.as_view(),
        name='invoice.time.ticket.list'
        ),
    url(regex=r'^ticket/(?P<pk>\d+)/time/add/$',
        view=TimeRecordCreateView.as_view(),
        name='invoice.time.create'
        ),
    url(regex=r'^time/$',
        view=TimeRecordListView.as_view(),
        name='invoice.time'
        ),
    url(regex=r'^time/(?P<pk>\d+)/edit/$',
        view=TimeRecordUpdateView.as_view(),
        name='invoice.time.update'
        ),
)
