# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib import admin

from .models import InvoiceSettings


class InvoiceSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(InvoiceSettings, InvoiceSettingsAdmin)
