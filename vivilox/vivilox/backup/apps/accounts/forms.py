from django import forms
from django.contrib.auth.models import User
from django.core import validators
from vivilox.apps.accounts.models import UserProfile
from vivilox.apps.tools.models import country as countrys
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError
from django.forms.widgets import RadioSelect

cho_type     = (("1","Client"),("2","Artist"),)	

# Custom Validators

def validate_username_unique(value):
	''' Custom validator for user uniqueness. '''
	if User.objects.filter(username=value).exists():
		raise ValidationError(u'The username "%s" is already taken.' % value)

def validate_email_unique(value):
	''' Custom validator for user uniqueness. '''
	if User.objects.filter(email=value).exists():
		raise ValidationError(u'The email "%s" is already taken.' % value)


class MyCostModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%.2f" % obj.cost

class LoginForm(forms.Form):
		username 		= forms.CharField(widget=forms.TextInput())
		password 		= forms.CharField(widget=forms.PasswordInput(render_value=False))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email","first_name","last_name"]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude =["user","user_type"]

class registerForm(forms.Form):
	# User type
	# user_type  = forms.ChoiceField(
	# 	widget=forms.RadioSelect(),
	# 	choices=cho_type,
	# 	required=True,
	# )
	user_type = forms.HiddenInput()
	#UserName Field
	username	=	forms.CharField(
		max_length=20,
		widget=forms.TextInput(
			attrs={'class':'span4','placeholder':'Insert here your UserName please.'},
		),
		required=True,
		min_length=3,
		validators=[validate_username_unique]
	)
	#Email Field
	email 	= 	forms.EmailField(
		max_length=255,
		widget=forms.TextInput(
			attrs={'class':'span4','placeholder':'Insert here your email please'},
		),
		required=True,
		validators=[validate_email_unique]

	)
	# Password & Re-Password
	password 	= 	forms.CharField(
		max_length=20,
		widget=forms.PasswordInput(
			attrs={'class':'span4','placeholder':'Insert your password'},
		),
		required=True,
	)
	repassword 	= 	forms.CharField(
		max_length=20,
		widget=forms.PasswordInput(
			attrs={'class':'span4','placeholder':'Insert again your password please'},
		),
		required=True,
	)
	# First Name
	first_name = forms.CharField(
		max_length=150,
		widget=forms.TextInput(
			attrs={'class':'span4','placeholder':'Insert here your First Name'},
		),
		required=True,
	)
	# Last Name
	last_name = forms.CharField(
		max_length=150,
		widget=forms.TextInput(
			attrs={'class':'span4','placeholder':'Insert here your Last Name'},
		),
		required=True,
	)

 	def clean(self):
 		''' Required custom validation for the form. '''
 		super(forms.Form,self).clean()
 		if 'password' in self.cleaned_data and 'repassword' in self.cleaned_data:
 			if self.cleaned_data['password'] != self.cleaned_data['repassword']:
 				self._errors['password'] = [u'Passwords must match.']
				self._errors['repassword'] = [u'Password must match']
		return self.cleaned_data



