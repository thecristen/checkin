from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Month(models.Model):
	month=models.CharField(max_length=100)
	active=models.BooleanField()
	url_month=models.CharField(max_length=100)
	short_name=models.CharField(max_length=50, default='')
	def __unicode__(self):
		return self.month
	def get_prior_months(self):
		return Month.objects.filter(id__lt=self.id).values_list('month', flat=True)

def getMonths():
	return Month.objects.filter(active=True).order_by('-id').values_list('month', flat=True)

