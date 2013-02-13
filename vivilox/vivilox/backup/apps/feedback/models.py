from django.db import models
from django.contrib.auth.models 	import User
from vivilox.apps.contests.models 	import contest,proposal
# Create your models here.


class feedback(models.Model):
	date 		= models.DateTimeField(auto_now=True)
	message		= models.TextField()
	client		= models.ForeignKey(User,related_name="Client")
	artist		= models.ForeignKey(User,related_name="Artist")
	contest 	= models.ForeignKey(contest)
	proposal 	= models.ForeignKey(proposal)
	sender      = models.ForeignKey(User,related_name="Sender")
	def __unicode__(self):
		return "%s" % self.date
