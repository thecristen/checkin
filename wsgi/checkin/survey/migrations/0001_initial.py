# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmplSizeCategory'
        db.create_table(u'survey_emplsizecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'survey', ['EmplSizeCategory'])

        # Adding model 'EmplSector'
        db.create_table(u'survey_emplsector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['EmplSector'])

        # Adding model 'Employer'
        db.create_table(u'survey_employer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('nr_employees', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('size_cat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.EmplSizeCategory'], null=True, blank=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.EmplSector'], null=True, blank=True)),
            ('is_parent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'survey', ['Employer'])

        # Adding model 'Commutersurvey'
        db.create_table(u'survey_commutersurvey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('home_location', self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0 0)', null=True, blank=True)),
            ('home_address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('work_location', self.gf('django.contrib.gis.db.models.fields.PointField')(default='POINT(0 0)', null=True, blank=True)),
            ('work_address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('distance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=1, blank=True)),
            ('duration', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=1, blank=True)),
            ('to_work_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('from_work_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('to_work_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('from_work_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('other_greentravel', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('employer', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('weight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=1, blank=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Commutersurvey'])

        # Adding model 'Schooldistrict'
        db.create_table(u'survey_schooldistrict', (
            ('districtid', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('distname', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=35)),
            ('startgrade', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('endgrade', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('distcode4', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('distcode8', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal(u'survey', ['Schooldistrict'])

        # Adding model 'School'
        db.create_table(u'survey_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, null=True, blank=True)),
            ('schid', self.gf('django.db.models.fields.CharField')(max_length=8, unique=True, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('town_mail', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('town', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('principal', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('grades', self.gf('django.db.models.fields.CharField')(max_length=70, null=True, blank=True)),
            ('schl_type', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('districtid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Schooldistrict'], null=True, blank=True)),
            ('survey_incentive', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('survey_active', self.gf('django.db.models.fields.BooleanField')()),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'survey', ['School'])

        # Adding model 'Studentsurvey'
        db.create_table(u'survey_studentsurvey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.School'])),
            ('teacher_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('teacher_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Studentsurvey'])

        # Adding model 'Studentgroup'
        db.create_table(u'survey_studentgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Studentsurvey'])),
            ('number', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('distance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=3, blank=True)),
            ('to_school_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('from_school_today', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('to_school_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('from_school_normally', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Studentgroup'])


    def backwards(self, orm):
        # Deleting model 'EmplSizeCategory'
        db.delete_table(u'survey_emplsizecategory')

        # Deleting model 'EmplSector'
        db.delete_table(u'survey_emplsector')

        # Deleting model 'Employer'
        db.delete_table(u'survey_employer')

        # Deleting model 'Commutersurvey'
        db.delete_table(u'survey_commutersurvey')

        # Deleting model 'Schooldistrict'
        db.delete_table(u'survey_schooldistrict')

        # Deleting model 'School'
        db.delete_table(u'survey_school')

        # Deleting model 'Studentsurvey'
        db.delete_table(u'survey_studentsurvey')

        # Deleting model 'Studentgroup'
        db.delete_table(u'survey_studentgroup')


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
        },
        u'survey.school': {
            'Meta': {'ordering': "['name']", 'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'districtid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Schooldistrict']", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'grades': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'principal': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'schid': ('django.db.models.fields.CharField', [], {'max_length': '8', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'schl_type': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'survey_active': ('django.db.models.fields.BooleanField', [], {}),
            'survey_incentive': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'town_mail': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'survey.schooldistrict': {
            'Meta': {'ordering': "['distname']", 'object_name': 'Schooldistrict'},
            'distcode4': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'distcode8': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'distname': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'districtid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'endgrade': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '35'}),
            'startgrade': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'survey.studentgroup': {
            'Meta': {'object_name': 'Studentgroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'from_school_normally': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'from_school_today': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Studentsurvey']"}),
            'to_school_normally': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'to_school_today': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'survey.studentsurvey': {
            'Meta': {'object_name': 'Studentsurvey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.School']"}),
            'teacher_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'teacher_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['survey']