from django.db import models


class country(models.Model):
	name    	 = models.CharField(max_length=100)
	visible 	 = models.BooleanField(default=True) 
	def __unicode__(self):
		return self.name
