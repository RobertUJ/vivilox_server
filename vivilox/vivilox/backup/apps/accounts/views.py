from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Models
from django.contrib.auth.models import User
from vivilox.apps.accounts.models import UserProfile
from vivilox.apps.contests.models import proposal,contest
from vivilox.apps.feedback.models import feedback
from vivilox.apps.store.models import item,purchases
from vivilox.apps.accounts.forms import UserForm,UserProfileForm,registerForm,LoginForm

@login_required
def profile_user(request):
    ''' User profile by user type ("1":"Client"),("2":"Artist"),("3":"Admin") '''
    if request.user.profile.user_type == "1":
    	_contest   = contest.objects.filter(user=request.user).order_by('-id')
        _purshased = purchases.objects.filter(user=request.user).order_by('-id')
        _feedback =  feedback.objects.filter(client=request.user).order_by('-id')
        ''' Falta el modelo de notificaciones '''
        ctx = {'profile':request.user.profile,'contests':_contest,'purchased':_purshased,'feedback':_feedback}
        return render_to_response('accounts/profile_client.html',ctx,context_instance=RequestContext(request))
    elif request.user.profile.user_type == "2":
        ''' Get image in store of user loguead '''
        myItems = item.objects.filter(user=request.user).order_by('-id')
        _feedback =  feedback.objects.filter(artist=request.user).order_by('-id')
        ''' Get Contest with User logued proposals '''
        _contest  = proposal.objects.filter(user=request.user).values('contest')
        myContest = contest.objects.filter(id__in=_contest)
        ''' Get purchased items '''
        myPurchasedItems = purchases.objects.filter(user=request.user).order_by('-id')
        ctx = {'profile':request.user.profile,'contests':myContest,'items':myItems,'purchased':myPurchasedItems,'feedback':_feedback}
        return render_to_response('accounts/profile_artist.html',ctx,context_instance=RequestContext(request))
    elif request.user.profile.user_type == "3":
    	return HttpResponseRedirect('/admin/')
    else:
    	return HttpResponseRedirect('/');

@login_required
def my_store(request):
	_store = item.objects.filter(user=request.user)
	ctx = {"items":_store,"profile":request.user.profile}
	return render_to_response("accounts/profile/artist/store.html",ctx,context_instance=RequestContext(request))



@login_required
def profile_contest(request):
	_type = request.user.profile.user_type
	if _type == "1":
		return show_contest_client(request)
	elif _type == "2":
		return show_proposal_artist(request)
	elif _type == "3":
		return HttpResponseRedirect("/admin/")
	else:
		return HttpResponseRedirect("/")

def show_contest_client(request):
	client = request.user
	_contest = contest.objects.filter(user=client).order_by("-id")
	ctx = {'contests':_contest,'profile':request.user.profile}
	return render_to_response('accounts/profile/client/contest.html',ctx,context_instance=RequestContext(request)) 

def show_proposal_artist(request):
	artist = request.user
	_contest  = proposal.objects.filter(user=artist).values('contest')
	myContest = contest.objects.filter(id__in=_contest)
	ctx = {'contests':myContest,'profile':request.user.profile}
	return render_to_response('accounts/profile/artist/contest.html',ctx,context_instance=RequestContext(request))


def images_purchased(request):
	_itemPurchesed = purchases.objects.filter(user=request.user).order_by('-id')
	
	paginator = Paginator(_itemPurchesed,4)
		
	try:
		page = request.GET.get('page')
	except ValueError:
		page = 1
	
	try:
		_itemPurchesed = paginator.page(page)
	except PageNotAnInteger, e:
		# If page is not an integer, deliver first page.
		_itemPurchesed = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		_itemPurchesed = paginator.page(paginator.num_pages)

	ctx = {"purchased":_itemPurchesed,"profile":request.user.profile} 
	user_type = request.user.profile.user_type
	if user_type 	== "1":
		template = "accounts/profile/client/purchased_images.html"
	elif user_type 	== "2":
		template = "accounts/profile/artist/purchased_images.html"
	else:
		return HttpResponseRedirect("/")

	return render_to_response(template,ctx,context_instance=RequestContext(request))


@login_required
def edit_profile(request):
	if request.method == "POST":
		uform = UserForm(request.POST,instance=request.user)
		pform = UserProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if uform.is_valid() and pform.is_valid():
			user = uform.save()
			pform.save()
			ctx = {'frmUser':uform,'frmProfile':pform,'msg':"Information stored successfully"}
			return render_to_response('forms/accounts/edit_user.html',ctx,context_instance=RequestContext(request))
	else:
		uform = UserForm(instance=request.user)
		pform = UserProfileForm(instance=request.user.profile)
	ctx = {'frmUser':uform,'frmProfile':pform}
	return render_to_response('forms/accounts/edit_user.html',ctx,context_instance=RequestContext(request))

def register_user(request):
	if request.user.is_authenticated():
		ctx = {'has_account':True}
		return render_to_response('forms/accounts/register_account.html',ctx,context_instance=RequestContext(request))
	if request.method == "POST":
		objForm = registerForm(request.POST)
		if objForm.is_valid():
			username_ = objForm.cleaned_data['username']
			email_ = objForm.cleaned_data['email']
			password_ = objForm.cleaned_data['password']
			new_user = User.objects.create_user(username= username_, email= email_,password=password_)
			new_user.is_staff = False
			new_user.first_name = objForm.cleaned_data['first_name']
			new_user.last_name 	= objForm.cleaned_data['last_name']
			new_user.save()
			''' Add data to UserProfile model '''
			usertype_ 	= objForm.cleaned_data["user_type"]
			new_profile = UserProfile.objects.get(user=new_user)
			new_profile.user_type = usertype_
			new_profile.save()
			return HttpResponseRedirect('/')
	else:
		objForm = registerForm()
	ctx = {'form':objForm}
	return render_to_response('forms/accounts/register_account.html',ctx,context_instance=RequestContext(request))


def login_view(request):
	strMsg =""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			objForm = LoginForm(request.POST)
			if objForm.is_valid():
				username = objForm.cleaned_data['username']
				password = objForm.cleaned_data['password']
				objUser = authenticate(username=username,password=password)
				if objUser is not None and objUser.is_active:
					login(request,objUser)
					return HttpResponseRedirect("/")
				else:
					strMsg = "Username Or Password Incorrect"
		objForm = LoginForm()
		ctx = {'form': objForm,'msg':strMsg}
		return render_to_response('forms/accounts/login.html',ctx,context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')