from django.forms import ModelForm 
from django import forms
from vivilox.apps.feedback.models import feedbacks


class formFeedBack(forms.ModelForm):
	class Meta:
		model = feedbacks
		exclude = ('date','client','artist','proposal','contest','sender',)