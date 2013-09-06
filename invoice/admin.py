from django.contrib import admin

from .models import InvoicePrintSettings


class InvoicePrintSettingsAdmin(admin.ModelAdmin):
    pass

admin.site.register(InvoicePrintSettings, InvoicePrintSettingsAdmin)
