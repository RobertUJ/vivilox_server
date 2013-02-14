from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

class category(models.Model):
	name  		= models.CharField(max_length=100)
	order 		= models.SmallIntegerField()
	active 		= models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

class item(models.Model):
	title 			= models.CharField(max_length=50)
	category 		= models.ForeignKey(category)
	description 	= models.TextField()
	image_sample	= models.ImageField(upload_to='store/images_samples')
	tags 			= models.CharField(max_length=255,help_text='Separated by commas')
	price			= models.FloatField()
	top_rated   	= models.BooleanField(default=False)
	license   		= models.BooleanField(default=False)
	user 			= models.ForeignKey(User)

	def __unicode__(self):
		return self.title

class expedient_item(models.Model):
	item 			= models.ForeignKey(item)
	name 			= models.CharField(max_length=255)
	image 			= models.ImageField(upload_to='store/expedients')
	def __unicode__(self):
		return self.item.title


class top_rated_cost(models.Model):
	cost   		= models.FloatField()

class purchases(models.Model):
	item 		= models.ForeignKey(item)
	date 		= models.DateTimeField(auto_now=True)
	user 		= models.ForeignKey(User)
	paid 		= models.BooleanField(default=False)
	released 	= models.BooleanField(default=False)
	def __unicode__(self):
		return self.item.title



class downloads(models.Model):
	user 			= models.ForeignKey(User)
	item_purchased	= models.ForeignKey(purchases)
	date			= models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return "%s %s | %s"%(self.user.first_name,self.user.last_name,self.item_purchased.item.title)