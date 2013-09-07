from django.contrib import admin

from .models import InvoiceSettings


class InvoiceSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(InvoiceSettings, InvoiceSettingsAdmin)
