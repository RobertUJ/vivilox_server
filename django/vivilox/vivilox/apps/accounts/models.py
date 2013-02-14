#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django import forms
from vivilox.apps.tools.models import country,province
from django.db.models.signals import post_save
from sorl.thumbnail import ImageField

cho_type      = (("1","Client"),("2","Artist"),("3","Admin"),)	

class UserProfile(models.Model):
	user          = models.ForeignKey(User, unique=True)
	phone         = models.CharField(max_length=20,null=True,blank=True)
	user_type     = models.CharField(max_length=10,choices=cho_type)
	image		  = models.ImageField(upload_to='accounts/profile',blank=True,null=True)
	country       = models.ForeignKey(country,blank=True,null=True)
	province	  = models.ForeignKey(province,blank=True,null=True)	
	business_name = models.CharField(max_length=250,blank=True,null=True)
	paypal_email  = models.EmailField(max_length=150,blank=True,null=True) 
	term_cond 	  = models.BooleanField()
	def __unicode__(self):
		_user = self.user
		if _user.first_name == "":
			return _user.username
		else:
			return "%s %s"%(_user.first_name,_user.last_name) 
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)



