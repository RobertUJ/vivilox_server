from django.forms import ModelForm 
from django.db import models
from django import forms
from vivilox.apps.store.models import category,item,top_rated_cost,expedient_item
from django.forms import ModelChoiceField



class add_item_store(forms.ModelForm):
	class Meta:
		model = item
		exclude = ['user',]


class frmExpedient(forms.ModelForm):
	class Meta:
		model = expedient_item
		exclude = ['item','name',]

			