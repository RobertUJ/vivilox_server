from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

from paypal.standard.forms import PayPalPaymentsForm
import uuid
from django.core.urlresolvers import reverse

# Agregar Formulario
from vivilox.apps.contests.forms import  addContestForm, addNewProposal,frmProposalFeedback,buildContest
from vivilox.apps.contests.models import contest,resource,proposal,category,proposal_feedback,cost,private_cost,top_rated_cost,duration
from vivilox.apps.feedback.models import feedbacks
# Librerias o herramientas para proceso de informacion

# from datetime import datetime
import time
import datetime
from django.core.mail import EmailMultiAlternatives # Para enviar HTML


# Decorators
def isClient(fn=None):
	def wrapper(request,*args, **kr):
		if request.user.profile.user_type != "1":
			# if msg:
			# 	_msg = msg
			# else:
			# 	_msg = "Sorry, you not have permissions for do this action."
			_msg= "Sorry, you not have permissions for do this action."
			ctx ={'message':_msg}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
		else:
			return fn(request, *args, **kr)
	return wrapper

def isArtist(fn=None):
	def wrapper(request, *args, **kr):
		if request.user.profile.user_type != "2":
			ctx ={'message':"Sorry, you not have permissions for do this action."}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
		else:
			return fn(request, *args, **kr)
	return wrapper


# ----------------------------------------------------------------------
@login_required
def new_contest(request):
	if request.user.profile.user_type != "1":
			_msg = "Sorry, you not have permissions for do this action."
			ctx ={'message':_msg}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
	if request.method == "POST":
		objForm = addContestForm(request.POST, request.FILES)
		if objForm.is_valid():
			form_uncommited = objForm.save(commit=False)
			form_uncommited.user = request.user
			form_uncommited.save()
			return HttpResponseRedirect('/')
	else:
		objForm = addContestForm()
	ctx = {'frmContest':objForm}
	return render_to_response('forms/contest/addContest.html',ctx,context_instance=RequestContext(request))



def view_all_contest(request):
	_objCategory = category.objects.filter(status=True)
	idCategory = 0
	if request.method == "POST":
		idCategory = int(request.POST['category'])
		if idCategory == 0:
			_objContest = contest.objects.filter(active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')
		else:
			_category = category.objects.get(id=idCategory)
			_objContest = contest.objects.filter(category=idCategory,active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')
	else:
		_objContest = contest.objects.filter(active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')	
	paginator = Paginator(_objContest,10)
	page = request.GET.get('page')
	try:
		obj_contest = paginator.page(page)
	except PageNotAnInteger:
		obj_contest = paginator.page(1)
	except EmptyPage:
		obj_contest = paginator.page(paginator.num_pages)


	_proposal_search = proposal.objects.filter(user=request.user)
	ctx = {'myC':1,'myproposals':_proposal_search, 'objContest':obj_contest,'objCategory':_objCategory,'idCat':idCategory,'date':datetime.datetime.now()}
	return render_to_response('contest/view_all.html',ctx,context_instance=RequestContext(request))

def view_top_contest(request):
	_objCategory = category.objects.filter(status=True)
	idCategory = 0
	if request.method == "POST":
		idCategory = int(request.POST['category'])
		if idCategory == 0:
			_objContest = contest.objects.filter(toprate=True,active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')
		else:
			_category = category.objects.get(id=idCategory)
			_objContest = contest.objects.filter(toprate=True,category=idCategory,active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')
	else:
		_objContest = contest.objects.filter(toprate=True,active=True,finished=False).annotate(num_proposals = Count('proposal')).order_by('toprate','-date_start')	
	paginator = Paginator(_objContest,10)
	page = request.GET.get('page')
	try:
		obj_contest = paginator.page(page)
	except PageNotAnInteger:
		obj_contest = paginator.page(1)
	except EmptyPage:
		obj_contest = paginator.page(paginator.num_pages)

	ctx = {'objContest':obj_contest,'objCategory':_objCategory,'idCat':idCategory,'date':datetime.datetime.now()}
	return render_to_response('contest/view_all.html',ctx,context_instance=RequestContext(request))


def contest_buyer(request,idBuyer):
	idClient = int(idBuyer)
	_objCategory = category.objects.filter(status=True)
	client = get_object_or_404(User,pk=idClient)
	idCategory = 0
	if request.method == "POST":
		idCategory = int(request.POST['category'])
		if idCategory == 0:
			_objContest = contest.objects.filter(active=True,user=client,finished=False).order_by('toprate','-date_start')
		else:
			_category = category.objects.get(id=idCategory)
			_objContest = contest.objects.filter(category=idCategory,user=client,active=True,finished=False).order_by('toprate','-date_start')
	else:
		_objContest = contest.objects.filter(active=True,user=client,finished=False).order_by('toprate','-date_start')	
	paginator = Paginator(_objContest,10)
	page = request.GET.get('page')
	try:
		obj_contest = paginator.page(page)
	except PageNotAnInteger:
		obj_contest = paginator.page(1)
	except EmptyPage:
		obj_contest = paginator.page(paginator.num_pages)

	ctx = {'objContest':obj_contest,'objCategory':_objCategory,'idCat':idCategory}
	return render_to_response('contest/view_all.html',ctx,context_instance=RequestContext(request))


def contest_details(request,idCont):
	idContest = int(idCont)
	_objContest = get_object_or_404(contest,pk=idContest)
	_objProposal = proposal.objects.filter(contest=idContest).order_by('-id')
	ctx = {'objContest':_objContest,'objProposal':_objProposal}
	return render_to_response('contest/contest_details.html',ctx,context_instance=RequestContext(request))

	
@login_required
@isArtist
def add_proposal(request,idCont):
	idContest = int(idCont)
	_objContest = contest.objects.get(id=idContest)
	if request.method == "POST":
		frmProposal = addNewProposal(request.POST,request.FILES)
		if frmProposal.is_valid():
			frm_Uncommited = frmProposal.save(commit=False)
			frm_Uncommited.user    = request.user
			frm_Uncommited.contest = _objContest
			frm_Uncommited.save()
			return HttpResponseRedirect( '/contest/detail/%s/%s'%(idCont,'#_proposal'))
	else:
		frmProposal = addNewProposal()
	ctx = {'form_Proposal':frmProposal,'objContest':_objContest}
	return render_to_response('forms/contest/addProposal.html',ctx,context_instance=RequestContext(request))

@login_required
@isClient
def flagWinner(request,idclient,idartist,idcontest,idproposal):
	_idclient = int(idclient)
	_idartist = int(idartist)
	_idcontest = int(idcontest)
	_idproposal = int(idproposal)
	
	_client 	= 	get_object_or_404(User,id=_idclient)
	_artist 	= 	get_object_or_404(User,id=_idartist)
	_contest 	= 	get_object_or_404(contest,id=_idcontest)
	_proposal   = 	get_object_or_404(proposal,id=_idproposal)

	_contest.finished = True
	_contest.save()

	_feedback 			= 	feedbacks(client = _client,artist = _artist,contest = _contest, proposal = _proposal,sender=_client)
	_feedback.message 	= "Hello!, your proposal %s has been chosen as the winner of the contest %s. Congratulations!!" % (_proposal.title,_contest.name)
	_feedback.save()

	''' Send Email '''
	subject = "Your proposal is the winner!!"
	to_admin = 'roberto@newemage.com'
	html_content = "Hello!, your proposal %s has been chosen as the winner of the contest %s. Congratulations!!" %(_proposal.title,_contest.name)
	msg = EmailMultiAlternatives(subject,html_content,'from@server.com',[to_admin,_client.email])
	msg.attach_alternative(html_content,'text/html') #Definimos el contenido como HTML
	msg.send() #enviamos el correo
	ctx = {'client':_client,'artist':_artist,'contest':_contest,'proposal':_proposal}
	return render_to_response('forms/contest/winner.html',ctx,context_instance=RequestContext(request))


@login_required
@isClient
def  get_categories(request):
	if request.method == "POST":
		if request.is_ajax():
			idCat = request.POST['idcat']	
			try:
				_cat = category.objects.get(id=idCat)
				respuesta = "%s" % _cat.description
			except category.DoesNotExist:
				respuesta =  "This category not exist"
			return HttpResponse(respuesta)			
	else:
		_categories = category.objects.all()
		ctx = {'cats':_categories}
		return render_to_response('forms/contest/categories.html',ctx,context_instance=RequestContext(request))


@login_required
@isClient
def buid_contest(request):
	idCat = int(request.session.get('cat', 0))
	objCat = get_object_or_404(category,pk=idCat)
	# Get costs by Category
	if objCat:
		objPrice = cost.objects.filter(category=objCat,status=True).order_by('cost')
		objCostPrivate = private_cost.objects.order_by('id')[0]
		objCostTopRate = top_rated_cost.objects.order_by('id')[0]
	else:
		objPrice = None
		objCostPrivate = None
		objCostTopRate = None

	# Save contest new
	if request.method == "POST":
		# contest,resource,proposal,category,proposal_feedback,cost,duration
		# user,name,category,industry,description,logo,cost,cost_custom,duration,date_start,date_end,private,toprate		active 			finished	total_cost 
		_frmContest = buildContest(request.POST,request.FILES)
		if _frmContest.is_valid():
			frmUncommited = _frmContest.save(commit=False)
			# form.cleaned_data['subject']
			subTotal = 0.00
			CostSelected = _frmContest.cleaned_data['cost']
			subTotal += float("%s"%CostSelected)

			print "Subtotal + CostoSeleccionado %s " % subTotal

			customCost = _frmContest.cleaned_data['cost_custom']
			
			if customCost:
				subTotal += float("%s"%customCost)
		
			print "Custom cost: %s" % customCost
			
			# get cost duration range
			
			idDur = int(request.POST['duration'])
			print idDur
			
			try:
				_duration = duration.objects.get(id=idDur)
				
			except:
				_duration = None
				
			if _duration:
				costDuration = _duration.cost
				# Sum Days for finish date
				days = _duration.duration
				diffDays = datetime.timedelta(days=days)
				now_ = datetime.datetime.now()
				dateFinish = now_ + diffDays
			else:
				costDuration = 0
				dateFinish = datetime.datetime.now()

			# Sum subTotal Duration 
			subTotal += costDuration
			frmUncommited.date_end = dateFinish

			# Is a Private Contest?
			isPrivate = _frmContest.cleaned_data['private']

			if isPrivate:
				costPrivate = objCostPrivate.cost
			else:
				costPrivate = 0
			subTotal += costPrivate

			# Is Top Rate Contest?
			isTopRate = _frmContest.cleaned_data['toprate']
			if isTopRate:
				costTopRate = objCostTopRate.cost
			else:
				costTopRate = 0
			subTotal += costTopRate
			# Add Total Cost
			frmUncommited.total_cost = subTotal
			frmUncommited.user = request.user
			frmUncommited.category = category.objects.get(id=idCat)
			frmUncommited.save()	
			ctx = {'infoContest':frmUncommited}
			return render_to_response('contest/resume.html',ctx,context_instance=RequestContext(request))
			return HttpResponseRedirect('/contest.all/')

		else:
			ctx = {'frmContest':_frmContest,'idCat':idCat,'cat':objCat,'costs':objPrice,'priv':objCostPrivate,'toprate':objCostTopRate}
	else:
		_frmContest = buildContest()
		ctx = {'frmContest':_frmContest,'idCat':idCat,'cat':objCat,'costs':objPrice,'priv':objCostPrivate,'toprate':objCostTopRate}
	
	return render_to_response('forms/contest/build_contest.html',ctx,context_instance=RequestContext(request))


@login_required
@isClient
def resume_contest(request):
	_contest = contest.objects.filter(user=request.user).order_by('-pk')[0]
	if not _contest.paid:
		ctx = {'infoContest':_contest}
		return render_to_response('contest/resume.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/contest.all/')


@login_required
@isClient
def define_category(request):
	if request.method == "POST":
		idCat = int(request.POST['id_cat'])
		request.session['cat'] = idCat
		return HttpResponseRedirect('/contest.build/')




@login_required
def proposal_details(request,idP):
	idProposal 	= int(idP) 
	objProposal = get_object_or_404(proposal,id=idProposal)

	if request.user.profile.user_type == "2":
		if objProposal.user != request.user:
			ctx = {'message':"Sorry, do not have permission to be here"}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
	elif request.user.profile.user_type == "1":
		if objProposal.contest.user != request.user:
			ctx = {'message':"Sorry, do not have permission to be here"}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))

	if request.method == "POST":
		objForm = frmProposalFeedback(request.POST)
		if objForm.is_valid():
			objUncommit = objForm.save(commit=False)
			objUncommit.proposal = objProposal
			objUncommit.client_p = objProposal.contest.user
			objUncommit.artist_p = objProposal.user
			objUncommit.sender   = request.user
			objUncommit.save()
	frmFeedback = frmProposalFeedback()		
	objFeedback = proposal_feedback.objects.filter(proposal=objProposal)		
	ctx = {'proposal':objProposal,'feedback':objFeedback,'fFeedback':frmFeedback}
	return render_to_response('proposals/proposal_details.html',ctx,context_instance=RequestContext(request))


@login_required
@isClient
def proposal_discard(request,idP):
	''' Funcion para marcar como descartada una propuesta '''
	idProposal = int(idP)
	objProposal = get_object_or_404(proposal,id=idProposal)
	if objProposal.contest.user == request.user:
		objProposal.discarded = True
		objProposal.save()
		return HttpResponseRedirect("/proposal.details/%s/"%idProposal)
	else:
		ctx = {'message':"Sorry, you not have permissions for do this action. <br/> This contest is not yours "}
		return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))		

	







# form_uncommited = objForm.save(commit=False)
# print datetime.now()
# form_uncommited.date_init = datetime.now()
# form_uncommited.active = True
# form_uncommited.user = request.user.id
# form_uncommited.date_create = datetime.now()
