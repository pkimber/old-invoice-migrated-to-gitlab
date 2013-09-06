from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
)

from braces.views import LoginRequiredMixin

from .forms import TimeRecordForm
from .models import TimeRecord
from crm.models import Ticket
from crm.views import CheckPermMixin


class TimeRecordCreateView(LoginRequiredMixin, CheckPermMixin, CreateView):
    form_class = TimeRecordForm
    model = TimeRecord

    def _get_ticket(self):
        pk = self.kwargs.get('pk')
        ticket = get_object_or_404(Ticket, pk=pk)
        self._check_perm(ticket.contact)
        return ticket

    def get_context_data(self, **kwargs):
        context = super(TimeRecordCreateView, self).get_context_data(**kwargs)
        context.update(dict(
            ticket=self._get_ticket(),
        ))
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ticket = self._get_ticket()
        self.object.user = self.request.user
        return super(TimeRecordCreateView, self).form_valid(form)
