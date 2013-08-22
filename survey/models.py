from django.contrib.gis.db import models
from django.db.models import permalink
from django.utils.text import slugify
from leaderboard.models import getMonths, Month

# lazy translation
from django.utils.translation import ugettext_lazy as _
from collections import namedtuple

# south introspection rules 
try:
	from south.modelsinspector import add_introspection_rules
	add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
	add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
	add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiLineStringField'])
except ImportError:
	pass


COMMUTER_MODES = (
		('c', _('Car')),
		('w', _('Walk')),
		('b', _('Bike')),
		('cp', _('Carpool')),
		('t', _('Transit (bus, subway, etc.)')),
		('o', _('Other (skate, canoe, etc.)')),
		('tc', _('Telecommuting')),
		)

STUDENT_MODES = (
		('w', _('Walk')),
		('b', _('Bike')),
		('sb', _('School Bus')),
		('fv', _('Family Vehicle (only students of one family)')),
		('cp', _('Carpool (with students from other families)')),
		('t', _('Transit (city bus, subway, etc.)')),
		('o', _('Other (skateboard, scooter, etc.)'))
		)

class EmplSizeCategory(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = _('Employer Size Category')
		verbose_name_plural = _('Employer Size Categories')

	def __unicode__(self):
		return self.name

class EmplSector(models.Model):
	name = models.CharField(max_length=100)
	parent = models.CharField(max_length=100, default=None, null=True, blank=True)
	class Meta:
		verbose_name = _('Employer Sector')
		verbose_name_plural = _('Employer Sectors')

	@property 
	def url_name(self):
		return slugify(self.name)
	def __unicode__(self):
		return self.name

def makeParent(empName):
	emp = Employer.objects.get(name=empName)
	emp.is_parent = True
	emp.save()

class Employer(models.Model):
	""" Greens Streets Initiative Employer list """
	name = models.CharField("Employer name", max_length=200)
	nr_employees = models.IntegerField("Number of employees", null=True, blank=True)
	active = models.BooleanField("Show in Commuter-Form", default=False)
	size_cat = models.ForeignKey(EmplSizeCategory, null=True, blank=True, verbose_name=u'Size Category')
	sector = models.ForeignKey(EmplSector, null=True, blank=True)
	is_parent = models.BooleanField(default=False)

	class Meta:
		verbose_name = _('Employer')
		verbose_name_plural = _('Employers')
		ordering = ['name']

	def __unicode__(self):
		return self.name
	@property
	def nr_surveys(self):
		return Commutersurvey.objects.filter(employer__exact=self.name).count()

	def get_surveys(self, month):
		if self.is_parent:
			sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
			if month != 'all':
				return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps)
			else:
				return Commutersurvey.objects.filter(month__in=getMonths(), employer__in=sectorEmps)
		else:
			if month != 'all':
				return Commutersurvey.objects.filter(month=month, employer__exact=self.name)
			else:
				return Commutersurvey.objects.filter(month__in=getMonths(), employer__exact=self.name)

	def get_nr_surveys(self, month):
		if self.is_parent:
			sectorEmps = Employer.objects.filter(sector=EmplSector.objects.get(parent=self.name)).values_list('name', flat=True)
			if month != 'all':
				return Commutersurvey.objects.filter(month=month, employer__in=sectorEmps).count()
			else:
				return Commutersurvey.objects.filter(month__in=getMonths(), employer__in=sectorEmps).count()
		else:
			if month != 'all':
				return Commutersurvey.objects.filter(month=month, employer__exact=self.name).count()
			else:
				return Commutersurvey.objects.filter(month__in=getMonths(), employer__exact=self.name).count()

	def get_new_surveys(self, month):
		monthObject = Month.objects.get(month=month)
		newSurveys = []
		previousMonths = monthObject.get_prior_months()
		for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
			if not Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
				newSurveys += [survey,]
		return newSurveys

	def get_returning_surveys(self, month):
		monthObject = Month.objects.get(month=month)
		returningSurveys = []
		previousMonths = monthObject.get_prior_months()
		for survey in Commutersurvey.objects.filter(month=month, employer=self.name):
			if Commutersurvey.objects.filter(email=survey.email, month__in=previousMonths).exists():
				returningSurveys += [survey,]
		return returningSurveys

class Commutersurvey(models.Model):
	"""
	Questions for adults about their commute work
	and Green Streets interest.
	"""

	month = models.CharField('Walk/Ride Day Month', max_length=50)

	home_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)') # default SRS 4326
	home_address = models.CharField(max_length=200)
	work_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)')
	work_address = models.CharField(max_length=200)

	distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
	duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)

	to_work_today = models.CharField(max_length=2, blank=False, null=True, choices=COMMUTER_MODES)
	from_work_today = models.CharField(max_length=2, blank=False, null=True, choices=COMMUTER_MODES)  
	to_work_normally = models.CharField(max_length=2, blank=False, null=True, choices=COMMUTER_MODES)
	from_work_normally = models.CharField(max_length=2, blank=False, null=True, choices=COMMUTER_MODES) 

	other_greentravel = models.BooleanField(default=False)

	name = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	#private = models.BooleanField(default=False)
	newsletter = models.BooleanField(default=True)
	employer = models.CharField('Employer', max_length=100, blank=False, null=True)
	weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)

	ip = models.IPAddressField('IP Address', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	objects = models.GeoManager()
	CheckinDict = {
			('c', 'c'):2, ('c', 'cp'):4, ('c', 'w'):4, ('c', 'b'):4, ('c', 't'):4, ('c', 'tc'):4, ('c', 'o'):1,
			('cp', 'c'):1, ('cp', 'cp'):3, ('cp', 'w'):4, ('cp', 'b'):4, ('cp', 't'):4, ('cp', 'tc'):4, ('cp', 'o'):1,
			('w', 'c'):1, ('w', 'cp'):3, ('w', 'w'):3, ('w', 'b'):3, ('w', 't'):3, ('w', 'tc'):3, ('w', 'o'):1,
			('b', 'c'):1, ('b', 'cp'):3, ('b', 'w'):3, ('b', 'b'):3, ('b', 't'):3, ('b', 'tc'):3, ('b', 'o'):1,
			('t', 'c'):1, ('t', 'cp'):3, ('t', 'w'):4, ('t', 'b'):4, ('t', 't'):3, ('t', 'tc'):4, ('t', 'o'):1,
			('tc', 'c'):1, ('tc', 'cp'):3, ('tc', 'w'):3, ('tc', 'b'):3, ('tc', 't'):3, ('tc', 'tc'):3, ('tc', 'o'):1,
			('o', 'c'):1, ('o', 'cp'):1, ('o', 'w'):1, ('o', 'b'):1, ('o', 't'):1, ('o', 'tc'):1, ('o', 'o'):1,
			}

	def __unicode__(self): 
		return u'%s' % (self.id)   

	class Meta:
		verbose_name = 'Commuter Survey'
		verbose_name_plural = 'Commuter Surveys'     

	@property
	def to_work_switch(self):
		if self.to_work_today is None:
			self.to_work_today = 'o'
		if self.to_work_normally is None:
			self.to_work_normally = 'o'
		return self.CheckinDict[(self.to_work_normally, self.to_work_today)]

	@property
	def from_work_switch(self):
		if self.from_work_today is None:
			self.from_work_today = 'o'
		if self.from_work_normally is None:
			self.from_work_normally = 'o'
		return self.CheckinDict[(self.from_work_normally, self.from_work_today)]


class Schooldistrict(models.Model):
	""" School Districts """
	districtid = models.IntegerField(primary_key=True)
	distname = models.CharField(max_length=35)
	slug = models.SlugField(max_length=35, unique=True)
	startgrade = models.CharField(max_length=2)
	endgrade = models.CharField(max_length=2)
	distcode4 = models.CharField(max_length=4)
	distcode8 = models.CharField(max_length=8)

	geometry = models.MultiPolygonField(srid=26986)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.distname

	class Meta:
		ordering = ['distname']


class School(models.Model):
	""" School """
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, blank=True, null=True)

	schid = models.CharField('School ID', max_length=8, blank=True, null=True, unique=True)
	address = models.CharField(max_length=150, blank=True, null=True)
	town_mail = models.CharField(max_length=25, blank=True, null=True)
	town = models.CharField('School Town', max_length=25, blank=True, null=True)
	state = models.CharField(max_length=2, blank=True, null=True)
	zip = models.CharField(max_length=10, blank=True, null=True)
	principal = models.CharField(max_length=50, blank=True, null=True)
	phone = models.CharField(max_length=15, blank=True, null=True)
	fax = models.CharField(max_length=15, blank=True, null=True)
	grades = models.CharField(max_length=70, blank=True, null=True)
	schl_type = models.CharField(max_length=3, blank=True, null=True)     
	districtid = models.ForeignKey('Schooldistrict', blank=True, null=True)

	survey_incentive = models.TextField(blank=True, null=True)
	survey_active = models.BooleanField('Is Survey School')

	# GeoDjango
	geometry = models.PointField(srid=26986)
	objects = models.GeoManager()

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = 'School'
		verbose_name_plural = 'Schools' 


class Studentsurvey(models.Model):
	""" To checkin entire classrooms or groups of students """

	month = models.CharField('Walk/Ride Day Month', max_length=50)

	school = models.ForeignKey(School, verbose_name='School')

	teacher_name = models.CharField(max_length=50, blank=True, null=True)
	teacher_email = models.EmailField()
	newsletter = models.BooleanField(default=False)

	ip = models.IPAddressField('IP Address', blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Studentsurvey')
		verbose_name_plural = _('Studentsurveys')

	def __unicode__(self):
		return "%s (%s)" % (self.teacher_email, self.month)


class Studentgroup(models.Model):
	""" Group of students to be checked in """

	teacher = models.ForeignKey(Studentsurvey)

	number = models.IntegerField('Number of students', default=1)
	distance = models.DecimalField('Travel distance', help_text='Average, in miles, e.g. 1.25', max_digits=10, decimal_places=3, blank=True, null=True)

	to_school_today = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES)
	from_school_today = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES) 

	to_school_normally = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES)
	from_school_normally = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES) 

	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = _('Studentgroup')
		verbose_name_plural = _('Studentgroups')

	def __unicode__(self):
		return "%s, %i students" % (self.teacher, self.number)

