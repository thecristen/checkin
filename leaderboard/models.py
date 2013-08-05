from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Month(models.Model):
    month=models.CharField(max_length=100)
    active=models.BooleanField()
    def __unicode__(self):
        return self.month

def getMonths():
        months = []
        for month in Month.objects.filter(active=True):
            months += [month.month,]
        return months

