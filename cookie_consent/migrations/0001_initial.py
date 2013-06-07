# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CookieGroup'
        db.create_table(u'cookie_consent_cookiegroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('varname', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_deletable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cookie_consent', ['CookieGroup'])

        # Adding model 'Cookie'
        db.create_table(u'cookie_consent_cookie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cookiegroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cookie_consent.CookieGroup'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('path', self.gf('django.db.models.fields.TextField')(default=u'/', blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cookie_consent', ['Cookie'])


    def backwards(self, orm):
        # Deleting model 'CookieGroup'
        db.delete_table(u'cookie_consent_cookiegroup')

        # Deleting model 'Cookie'
        db.delete_table(u'cookie_consent_cookie')


    models = {
        u'cookie_consent.cookie': {
            'Meta': {'ordering': "[u'-created']", 'object_name': 'Cookie'},
            'cookiegroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cookie_consent.CookieGroup']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'path': ('django.db.models.fields.TextField', [], {'default': "u'/'", 'blank': 'True'})
        },
        u'cookie_consent.cookiegroup': {
            'Meta': {'ordering': "[u'ordering']", 'object_name': 'CookieGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deletable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'varname': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['cookie_consent']