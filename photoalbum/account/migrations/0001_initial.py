# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table('account_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255, unique=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, default='M')),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('account', ['Account'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table('account_account')


    models = {
        'account.account': {
            'Meta': {'object_name': 'Account'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'unique': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'M'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['account']