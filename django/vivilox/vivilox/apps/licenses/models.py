from django.db import models
from django.template.defaultfilters import slugify

class license(models.Model):
	name 		=  models.CharField(max_length=255,null=False,blank=False,unique=True,verbose_name=u'Client Name')
	slug		=  models.SlugField(max_length=255,null=True,blank=True,editable=False,unique=True,help_text="This value is automatically filled")
	text		=  models.TextField()
	active		=  models.BooleanField(default=True)

	def __unicode__(self):
		return str(self.name)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(license,self).save(*args,**kwargs)




