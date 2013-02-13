from django.forms import ModelForm 
from django import forms
from vivilox.apps.feedback.models import feedback


class formFeedBack(forms.ModelForm):
	class Meta:
		model = feedback
		exclude = ('date','client','artist','proposal','contest','sender',)