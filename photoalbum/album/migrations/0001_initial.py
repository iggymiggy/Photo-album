# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table('album_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Account'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('firstpage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('public_hash', self.gf('django.db.models.fields.CharField')(unique=True, default='cd4911bc9b2711e3b7a008002708055a', max_length=32)),
        ))
        db.send_create_signal('album', ['Album'])

        # Adding model 'Page'
        db.create_table('album_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Album'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('layout', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('album', ['Page'])

        # Adding model 'Picture'
        db.create_table('album_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['album.Page'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, default='')),
            ('caption', self.gf('django.db.models.fields.TextField')(default='')),
            ('price', self.gf('django.db.models.fields.DecimalField')(decimal_places=2, default=0, max_digits=10)),
        ))
        db.send_create_signal('album', ['Picture'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table('album_album')

        # Deleting model 'Page'
        db.delete_table('album_page')

        # Deleting model 'Picture'
        db.delete_table('album_picture')


    models = {
        'account.account': {
            'Meta': {'object_name': 'Account'},
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': "'M'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'album.album': {
            'Meta': {'object_name': 'Album'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'firstpage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Account']"}),
            'public_hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'default': "'cd4a40789b2711e3b7a008002708055a'", 'max_length': '32'})
        },
        'album.page': {
            'Meta': {'object_name': 'Page'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'layout': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'album.picture': {
            'Meta': {'object_name': 'Picture'},
            'caption': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['album.Page']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'decimal_places': '2', 'default': '0', 'max_digits': '10'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'default': "''"})
        }
    }

    complete_apps = ['album']