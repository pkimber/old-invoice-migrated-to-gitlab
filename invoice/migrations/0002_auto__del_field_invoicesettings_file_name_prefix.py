from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'InvoiceSettings.file_name_prefix'
        db.delete_column(u'invoice_invoicesettings', 'file_name_prefix')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'InvoiceSettings.file_name_prefix'
        raise RuntimeError("Cannot reverse this migration. 'InvoiceSettings.file_name_prefix' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'InvoiceSettings.file_name_prefix'
        db.add_column(u'invoice_invoicesettings', 'file_name_prefix',
                      self.gf('django.db.models.fields.CharField')(max_length=10),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crm.contact': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Contact'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Industry']", 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'crm.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crm.priority': {
            'Meta': {'ordering': "['-level', 'name']", 'object_name': 'Priority'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'crm.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'complete_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Priority']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'invoice.invoiceline': {
            'Meta': {'unique_together': "(('invoice', 'line_number'),)", 'object_name': 'InvoiceLine'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['invoice.Invoice']"}),
            'line_number': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'net': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'vat': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'vat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'})
        },
        u'invoice.invoicesettings': {
            'Meta': {'object_name': 'InvoiceSettings'},
            'footer': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_and_address': ('django.db.models.fields.TextField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'vat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        u'invoice.timerecord': {
            'Meta': {'ordering': "['date_started', 'start_time']", 'object_name': 'TimeRecord'},
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_line': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['invoice.InvoiceLine']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crm.Ticket']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['invoice']