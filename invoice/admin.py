# -*- encoding: utf-8 -*-
from django.contrib import admin

from .models import (
    InvoiceSettings,
    TimeCode,
)


class InvoiceSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(InvoiceSettings, InvoiceSettingsAdmin)


class TimeCodeAdmin(admin.ModelAdmin):
    pass

admin.site.register(TimeCode, TimeCodeAdmin)
