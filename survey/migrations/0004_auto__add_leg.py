# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Leg'
        db.create_table(u'survey_leg', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mode', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('direction', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('longest', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'survey', ['Leg'])

        # Adding M2M table for field legs on 'Commutersurvey'
        m2m_table_name = db.shorten_name(u'survey_commutersurvey_legs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('commutersurvey', models.ForeignKey(orm[u'survey.commutersurvey'], null=False)),
            ('leg', models.ForeignKey(orm[u'survey.leg'], null=False))
        ))
        db.create_unique(m2m_table_name, ['commutersurvey_id', 'leg_id'])


    def backwards(self, orm):
        # Deleting model 'Leg'
        db.delete_table(u'survey_leg')

        # Removing M2M table for field legs on 'Commutersurvey'
        db.delete_table(db.shorten_name(u'survey_commutersurvey_legs'))


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
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'null': 'True', 'blank': 'True'}),
            'home_address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'home_location': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "'POINT(0 0)'", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'legs': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['survey.Leg']", 'symmetrical': 'False'}),
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
        u'survey.leg': {
            'Meta': {'object_name': 'Leg'},
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longest': ('django.db.models.fields.BooleanField', [], {}),
            'mode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        }
    }

    complete_apps = ['survey']