from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoice_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')()),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Contact'])),
            ('pdf', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('invoice', ['Invoice'])

        # Adding model 'InvoiceSettings'
        db.create_table('invoice_invoicesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('file_name_prefix', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('vat_number', self.gf('django.db.models.fields.CharField')(max_length=12, blank=True)),
            ('name_and_address', self.gf('django.db.models.fields.TextField')()),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('footer', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('invoice', ['InvoiceSettings'])

        # Adding model 'InvoiceLine'
        db.create_table('invoice_invoiceline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoice.Invoice'])),
            ('line_number', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('net', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('vat_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('vat', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('invoice', ['InvoiceLine'])

        # Adding unique constraint on 'InvoiceLine', fields ['invoice', 'line_number']
        db.create_unique('invoice_invoiceline', ['invoice_id', 'line_number'])

        # Adding model 'TimeRecord'
        db.create_table('invoice_timerecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crm.Ticket'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_started', self.gf('django.db.models.fields.DateField')()),
            ('start_time', self.gf('django.db.models.fields.TimeField')()),
            ('end_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('billable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invoice_line', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoice.InvoiceLine'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('invoice', ['TimeRecord'])


    def backwards(self, orm):
        # Removing unique constraint on 'InvoiceLine', fields ['invoice', 'line_number']
        db.delete_unique('invoice_invoiceline', ['invoice_id', 'line_number'])

        # Deleting model 'Invoice'
        db.delete_table('invoice_invoice')

        # Deleting model 'InvoiceSettings'
        db.delete_table('invoice_invoicesettings')

        # Deleting model 'InvoiceLine'
        db.delete_table('invoice_invoiceline')

        # Deleting model 'TimeRecord'
        db.delete_table('invoice_timerecord')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'crm.contact': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Contact'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hourly_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Industry']", 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'crm.industry': {
            'Meta': {'ordering': "['name']", 'object_name': 'Industry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'crm.priority': {
            'Meta': {'ordering': "['-level', 'name']", 'object_name': 'Priority'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'crm.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'complete': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'complete_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Priority']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Contact']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pdf': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'})
        },
        'invoice.invoiceline': {
            'Meta': {'unique_together': "(('invoice', 'line_number'),)", 'object_name': 'InvoiceLine'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoice.Invoice']"}),
            'line_number': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'net': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'vat': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'vat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'})
        },
        'invoice.invoicesettings': {
            'Meta': {'object_name': 'InvoiceSettings'},
            'file_name_prefix': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'footer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_and_address': ('django.db.models.fields.TextField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'vat_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'vat_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'})
        },
        'invoice.timerecord': {
            'Meta': {'ordering': "['date_started', 'start_time']", 'object_name': 'TimeRecord'},
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_line': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.InvoiceLine']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crm.Ticket']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['invoice']
