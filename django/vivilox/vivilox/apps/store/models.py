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
	title 			= models.CharField(max_length=50,verbose_name="Title")
	category 		= models.ForeignKey(category,verbose_name="Category")
	description 	= models.TextField(verbose_name="Description")
	image_sample	= models.ImageField(upload_to='store/images_samples',verbose_name="Thubnail preview (upload a low resolution thumbnail of your artwork)",help_text="")
	tags 			= models.CharField(max_length=255,help_text='Separated by commas',verbose_name="Tags")
	price			= models.FloatField(verbose_name="Price")
	top_rated   	= models.BooleanField(default=False,verbose_name="Top Rated",help_text="(Top rated pieces appear in the top rated section to attarct more buyers)")
	license   		= models.BooleanField(default=False,verbose_name="License")
	date_time		= models.DateTimeField(auto_now_add=True)
	user 			= models.ForeignKey(User,verbose_name="")
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



class top_rated_text(models.Model):
	text = models.TextField()
	date = models.DateField(auto_now_add=True)
	class Meta:
	    verbose_name = "Top Rated text"
	    verbose_name_plural = "Top Rated text for item store"

	def __unicode__(self):
		return "%s" % self.date

class license_text(models.Model):
	text = models.TextField()
	date = models.DateField(auto_now_add=True)
	class Meta:
	    verbose_name = "License Text"
	    verbose_name_plural = "License text for item store"

	def __unicode__(self):
		return "%s" % self.date