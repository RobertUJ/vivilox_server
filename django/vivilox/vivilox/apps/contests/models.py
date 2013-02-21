#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from sorl.thumbnail import ImageField

class category(models.Model):
	name 		= models.CharField(max_length=200)
	description = models.TextField(null=True,blank=True)
	status 		= models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class industry(models.Model):
	name 		= models.CharField(max_length=200)
	description = models.TextField(null=True,blank=True)
	status 		= models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class top_rated_cost(models.Model):
	cost 		= models.FloatField()
	description = models.TextField(null=True,blank=True)
	def __unicode__(self):
		return "%2f"% (self.cost)

class private_cost(models.Model):
	cost 		= models.FloatField()
	description = models.TextField(null=True,blank=True)
	def __unicode__(self):
		return "%2f"% (self.cost)

class cost(models.Model):
	cost   		= 	models.FloatField()
	order		= 	models.IntegerField()
	description = 	models.TextField(null=True,blank=True)
	category 	=   models.ForeignKey(category)
	status 		=	models.BooleanField(default=True)	
	def __unicode__(self):
		return "%2f"% (self.cost)

class duration(models.Model):
	duration 	= models.IntegerField(help_text='Insert number of days')
	cost 		= models.FloatField()
	description = models.TextField(null=True,blank=True)
	order 		= models.IntegerField()
	status 		= models.BooleanField(default=True)
	def __unicode__(self):
		if self.cost == 0:
			return "%s days ::  Free"%(self.duration)
		else:
			return "%s days ::  + $ %s dlls"%(self.duration,self.cost)

class contest(models.Model):
	user 	 	= models.ForeignKey(User)
	name 		= models.CharField(max_length=200,unique=True)
	category 	= models.ForeignKey(category)
	industry	= models.ForeignKey(industry,blank=True,null=True)
	description	= models.TextField()
	logo 		= models.ImageField(upload_to='contests/logos',blank=True,null=True)
	cost 		= models.ForeignKey(cost)
	cost_custom = models.FloatField(null=True,blank=True)
	duration	= models.ForeignKey(duration)
	web_site	= models.URLField(verify_exists=True,max_length=150,blank=True,null=True)
	date_start  = models.DateTimeField(auto_now_add=True)
	date_end    = models.DateTimeField(blank=True,null=True)
	private 	= models.BooleanField(default=False)
	toprate 	= models.BooleanField(default=False)
	active 		= models.BooleanField(default=True)
	paid		= models.BooleanField(default=False)
	finished	= models.BooleanField(default=False)
	total_cost  = models.FloatField(blank=True,null=True)	
	def __unicode__(self):
		return self.name

class resource(models.Model):
	contest_id 	= models.ForeignKey(contest)
	name 		= models.CharField(max_length=100)
	resource 	= models.FileField(upload_to='contests/resource')
	status 		= models.BooleanField(default=True)
	date 		= models.DateField()	
	def __unicode__(self):
		return self.name

# Seccion dedicada a las propuestas de cada contest
class proposal(models.Model):
	title		= models.CharField(max_length=150)
	resource 	= models.FileField(upload_to='contests/proposal')
	comment		= models.TextField()
	status		= models.BooleanField(default=True)
	date 		= models.DateField(auto_now_add=True)
	discarded	= models.BooleanField(default=False)
	user 		= models.ForeignKey(User)
	contest 	= models.ForeignKey(contest)
	def __unicode__(self):
		return self.title


class proposal_feedback(models.Model):
	feedback 		= models.TextField()
	proposal 		= models.ForeignKey(proposal)
	client_p	 	= models.ForeignKey(User,related_name="Artist_Proposal")
	artist_p		= models.ForeignKey(User,related_name="Client_Proyect")
	datetime		= models.DateTimeField(auto_now_add=True)
	sender 			= models.ForeignKey(User,related_name="User_Sender")
	def __unicode__(self):
		return "%s ==> %s" % (self.proposal.contest.name,self.proposal.title)






		