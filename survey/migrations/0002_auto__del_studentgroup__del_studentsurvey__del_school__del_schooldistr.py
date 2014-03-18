# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Studentgroup'
        db.delete_table(u'survey_studentgroup')

        # Deleting model 'Studentsurvey'
        db.delete_table(u'survey_studentsurvey')

        # Deleting model 'School'
        db.delete_table(u'survey_school')

        # Deleting model 'Schooldistrict'
        db.delete_table(u'survey_schooldistrict')


    def backwards(self, orm):
        # Adding model 'Studentgroup'
        db.create_table(u'survey_studentgroup', (
            ('distance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('from_school_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('to_school_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Studentsurvey'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('from_school_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('to_school_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'survey', ['Studentgroup'])

        # Adding model 'Studentsurvey'
        db.create_table(u'survey_studentsurvey', (
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.School'])),
            ('teacher_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('teacher_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'survey', ['Studentsurvey'])

        # Adding model 'School'
        db.create_table(u'survey_school', (
            ('town', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('districtid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Schooldistrict'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, null=True, blank=True)),
            ('schid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('grades', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('schl_type', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('survey_incentive', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('survey_active', self.gf('django.db.models.fields.BooleanField')()),
            ('town_mail', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('principal', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['School'])

        # Adding model 'Schooldistrict'
        db.create_table(u'survey_schooldistrict', (
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('distcode8', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('districtid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('distcode4', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('distname', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('endgrade', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('startgrade', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=35, unique=True)),
        ))
        db.send_create_signal(u'survey', ['Schooldistrict'])


    models = {
        u'survey.commutersurvey': {
            'Meta': {'object_name': 'Commutersurvey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'duration': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '1', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'employer': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'from_work_normally': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'from_work_today': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'home_location': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "'POINT(0 0)'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'other_greentravel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'to_work_normally': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'to_work_today': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'weight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '1', 'blank': 'True'}),
            'work_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'work_location': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "'POINT(0 0)'", 'null': 'True', 'blank': 'True'})
        },
        u'survey.employer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Employer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_parent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'nr_employees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.EmplSector']", 'null': 'True', 'blank': 'True'}),
            'size_cat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.EmplSizeCategory']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.emplsector': {
            'Meta': {'object_name': 'EmplSector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'survey.emplsizecategory': {
            'Meta': {'object_name': 'EmplSizeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['survey']