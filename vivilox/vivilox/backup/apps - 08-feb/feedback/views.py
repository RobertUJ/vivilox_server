#Http
from django.shortcuts 	import render_to_response, get_object_or_404
from django.template 	import RequestContext
from django.http		import HttpResponseRedirect
from django.http 		import Http404
#Decorators
from django.contrib.auth.decorators import login_required
#Models
from vivilox.apps.feedback.models 	import feedbacks
from django.contrib.auth.models 	import User
from vivilox.apps.contests.models 	import proposal,contest
#Forms
from vivilox.apps.feedback.forms 	import formFeedBack
#Libs & Tools
from datetime import datetime
from django.core.mail import EmailMultiAlternatives 


@login_required
def view_feedback(request):
	''' Obtiene el tipo de usuario y filtra los mensajes enviados para el 
		("1","Client"),("2","Artist"),("3","Admin")	
	'''
	_user = request.user
	user_type = request.user.profile.user_type
	idContest = 0
	if request.method == "POST":
		idContest = int(request.POST['idContest'])
		if idContest == 0:
			if user_type == "1":
				_feedback = feedbacks.objects.filter(client=_user)
			elif user_type == "2":
				_feedback = feedbacks.objects.filter(artist=_user)
			elif user_type == "3":
				return HttpResponseRedirect('/admin/')
			else:
				return HttpResponseRedirect('/')
		else:
			_contest = contest.objects.get(id=idContest)
			contest_name = _contest.id			
			if user_type == "1":
				_feedback = feedbacks.objects.filter(client=_user,contest=_contest)
			elif user_type == "2":
				_feedback = feedbacks.objects.filter(artist=_user,contest=_contest)
			elif user_type == "3":
				return HttpResponseRedirect('/admin/')
			else:
				return HttpResponseRedirect('/')
	else:
		if user_type == "1":
			_feedback = feedbacks.objects.filter(client=_user)
		elif user_type == "2":
			_feedback = feedbacks.objects.filter(artist=_user)
		elif user_type == "3":
			return HttpResponseRedirect('/admin/')
		else:
			return HttpResponseRedirect('/')
	_contest  = proposal.objects.filter(user=request.user).values('contest')
	myContest = contest.objects.filter(id__in=_contest)
	if user_type == "2":
		_contest = myContest
	else:
		_contest = contest.objects.filter(user=request.user)
	ctx = {'fdb':_feedback,'contests':_contest,'idCon':idContest}
	return render_to_response('feedback/feedback.html',ctx,context_instance=RequestContext(request))


@login_required
def feedback_add(request,idclient,idartist,idcontest,idproposal):
	_idclient = int(idclient)
	_idartist = int(idartist)
	_idcontest = int(idcontest)
	_idproposal = int(idproposal)
	if request.method == "POST":
	    frmFeedback = formFeedBack(request.POST)
            if frmFeedback.is_valid():
            	frmNewUncommit = frmFeedback.save(commit=False)
            	frmNewUncommit.client 	= User.objects.get(id=_idclient)
            	frmNewUncommit.artist 	= User.objects.get(id=_idartist)
            	frmNewUncommit.contest 	= contest.objects.get(id=_idcontest)
            	frmNewUncommit.proposal = proposal.objects.get(id=_idproposal)
            	frmNewUncommit.sender 	= request.user
            	frmNewUncommit.save()
            	ctx = {'frmFeedBack':frmFeedback,'message':'Your feedback has been sent!'}
            	return render_to_response('forms/feedback/add_feedback.html',ctx,context_instance=RequestContext(request))
        else:
    	    frmFeedback = formFeedBack()
    	    ctx = {'frmFeedBack':frmFeedback}
    	    return render_to_response('forms/feedback/add_feedback.html',ctx,context_instance=RequestContext(request))


@login_required
def feedback_delete(request,idFeedback):
	_idFeedback = int(idFeedback)
	print _idFeedback
	instanceFeedback = get_object_or_404(feedbacks,pk=_idFeedback)
	instanceFeedback.delete()
	return HttpResponseRedirect('/profile/feedback/')
