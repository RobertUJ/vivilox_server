from django.forms import ModelForm 
from django.db import models
from django import forms
from vivilox.apps.contests.models import contest, cost, duration, proposal,proposal_feedback
from django.forms import ModelChoiceField

class MyCostModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "$ %.2f USD" % obj.description


class buildContest(forms.ModelForm):
	m_costs = cost.objects.filter(status=True).order_by('order', 'cost')

  	cost = MyCostModelChoiceField(queryset=m_costs,
 								  widget=forms.RadioSelect(),
 								  empty_label=None)
	class Meta:
		model = contest
		exclude = ['industry','date_finish','user','active','finished','category','date_end','total_cost','paid',]



class editContest(forms.ModelForm):
	m_costs = cost.objects.filter(status=True).order_by('order', 'cost')

  	cost = MyCostModelChoiceField(queryset=m_costs,
 								  widget=forms.RadioSelect(),
 								  empty_label=None)
	class Meta:
		model = contest
		exclude = ['industry','date_finish','user','active','finished','category','date_end','total_cost','paid',]




class addContestForm(forms.ModelForm):
	name = forms.CharField(
 		max_length=255,
 		widget=forms.TextInput(attrs={'class':'span8','placeholder':'Insert here your project name please.'},
 		),
 	)
 	description = forms.CharField(
 		widget=forms.Textarea(attrs={'class':'span8','placeholder':'Insert a description for the new contest'})
	)
 	m_costs = cost.objects.filter(status=True).order_by('order', 'cost')
  	m_duration = duration.objects.filter(status=True).order_by('order')
 	
 	cost = MyCostModelChoiceField(queryset=m_costs,
 								  widget=forms.RadioSelect(),
 								  empty_label=None)

 	duration = forms.ModelChoiceField(queryset=m_duration,
 								  widget=forms.RadioSelect(),
								  empty_label=None)
	class Meta:
		model = contest
		exclude = ('industry','date_finish','user','active','finished')
	class costModelChoiceField(ModelChoiceField):
		def label_from_instance(self, obj):
			return "%s" % obj.cost


class addNewProposal(forms.ModelForm):
	class Meta:
		model = proposal
		exclude = ('date','user','contest','status','discarded')

class frmProposalFeedback(forms.ModelForm):
	class Meta:
		model = proposal_feedback
		exclude = ['proposal','client_p','artist_p','datetime','sender']



