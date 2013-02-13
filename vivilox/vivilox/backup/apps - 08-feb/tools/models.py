#encoding:utf-8

from django.db import models
from vivilox.apps.store.models import category as cat_store


class country(models.Model):
	name    	 = models.CharField(max_length=100)
	visible 	 = models.BooleanField(default=True) 
	def __unicode__(self):
		return self.name

class province(models.Model):
	country = models.ForeignKey(country)
	name = models.CharField(max_length=50)
	abbrev = models.CharField(max_length=10)
	def __unicode__(self):
		return ('%s (%s)') % (self.name,self.abbrev)

class tax(models.Model):
	province = models.ForeignKey(province)
	tax_name = models.CharField(max_length=50)
	amount   = models.FloatField(help_text='% of tax')
	def __unicode__(self):
		return ("%s -- %s   %s")%(self.province,str(self.amount) + "%",self.tax_name)

class sale_percentage(models.Model):
	porcentage = models.FloatField(verbose_name=u'Sale Porcentage',help_text='% of sales')
	category   = models.ForeignKey(cat_store)
	def __unicode__(self):
		return "%s" % self.category	



