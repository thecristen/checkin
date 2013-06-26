from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Month(models.Model):
    month=models.CharField(max_length=100)
    url_month=models.CharField(max_length=100)
    def __unicode__(self):
        return self.month

