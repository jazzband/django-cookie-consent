# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LogItem'
        db.create_table(u'cookie_consent_logitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action', self.gf('django.db.models.fields.IntegerField')()),
            ('cookiegroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cookie_consent.CookieGroup'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'cookie_consent', ['LogItem'])


    def backwards(self, orm):
        # Deleting model 'LogItem'
        db.delete_table(u'cookie_consent_logitem')


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
        },
        u'cookie_consent.logitem': {
            'Meta': {'ordering': "[u'-created']", 'object_name': 'LogItem'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'cookiegroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cookie_consent.CookieGroup']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['cookie_consent']