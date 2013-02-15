from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Agregar Formulario
from vivilox.apps.store.models import category, item, top_rated_cost, expedient_item, purchases,downloads
from vivilox.apps.store.models import top_rated_text,license_text
#Carga de formularios
from vivilox.apps.store.forms import add_item_store,frmExpedient
# Librerias o herramientas para proceso de informacion
from datetime import datetime
from django.db.models import Count


# Decorators
def isClient(fn):
	def wrapper(request, *args, **kr):
		if request.user.profile.user_type != "1":
			ctx ={'message':"Sorry, you not have permissions for do this action."}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
		else:
			return fn(request, *args, **kr)
	return wrapper

def isArtist(fn):
	def wrapper(request, *args, **kr):
		if request.user.profile.user_type != "2":
			ctx ={'message':"Sorry, you not have permissions for do this action."}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
		else:
			return fn(request, *args, **kr)
	return wrapper

# ----------------------------------------------------------------------


def store(request):
	if request.method == "POST":
		idCategory = int(request.POST['category'])
		print idCategory

		if idCategory == 0:
		 	_items	= item.objects.all().annotate(sold = Count('purchases')).order_by('-id')
		else:
		 	_items	= item.objects.filter(category = idCategory).annotate(sold = Count('purchases')).order_by('-id')
		
		paginator = Paginator(_items,12)
		
		try:
			page = request.GET.get('page')
		except ValueError:
			page = 1
		
		try:
			_items = paginator.page(page)
		except PageNotAnInteger, e:
			# If page is not an integer, deliver first page.
			_items = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			_items = paginator.page(paginator.num_pages)
		
		_category 	= category.objects.all()
		ctx = {'objItems':_items, 'objCategory':_category,'idCat':idCategory}
		return render_to_response('store/store.html',ctx,context_instance=RequestContext(request))
	else:
		_items 	= item.objects.all().annotate(sold = Count('purchases')).order_by('-id')
		paginator = Paginator(_items,12)
		
		try:
			page = request.GET.get('page')
		except ValueError:
			page = 1
		
		try:
			_items = paginator.page(page)
		except PageNotAnInteger, e:
			# If page is not an integer, deliver first page.
			_items = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			_items = paginator.page(paginator.num_pages)

		idCategory = 0	
		_category 	= category.objects.all()
		ctx = {'objItems':_items, 'objCategory':_category,'idCat':idCategory}
		return render_to_response('store/store.html',ctx,context_instance=RequestContext(request))


@login_required
def image_details(request,idImg):
	idItem = int(idImg)
	_objItem = item.objects.get(pk=idItem)
	try:
		_objExpedient = expedient_item.objects.filter(item=_objItem)
	except expedient_item.DoesNotExist:
		_objExpedient = None

	try:
		_objPurchased = purchases.objects.filter(item=_objItem)
	except purchases.DoesNotExist:
		_objPurchased = None

	ctx = {'item':_objItem,'expedient':_objExpedient,'purchases':_objPurchased}
	return render_to_response('store/image_details.html',ctx,context_instance=RequestContext(request))


@login_required
@isArtist
def add_item(request):
	if request.method == 'POST':
		frmItem = add_item_store(request.POST,request.FILES)
		if frmItem.is_valid():
			frm_Uncommited 		= frmItem.save(commit=False)
			frm_Uncommited.user = request.user
			frm_Uncommited.save()
			request.session['item_id_added'] = frm_Uncommited.id
			print request.session['item_id_added']
			return HttpResponseRedirect("/store/expedient/new/")			
	else:
		frmItem = add_item_store()


	_text_top_rated = top_rated_text.objects.all().order_by("-date")[0]
	_license_text = license_text.objects.all().order_by("-date")[0]

	ctx = {'objForm':frmItem,'objTextTop':_text_top_rated,'objTextLicense':_license_text}
	return render_to_response('forms/store/add_item_store.html',ctx,context_instance=RequestContext(request))


@login_required
def add_item_expedient(request):
	if request.method == "POST":
		if not request.FILES:
			frmExp = frmExpedient()
			ctx = {'frmExped':frmExp,'msg':"This input is required"}
			return render_to_response('forms/store/add_expedient.html',ctx,context_instance=RequestContext(request))

		image_items = request.FILES.getlist('image')
		for i in image_items:
			try:
				item_instance = item.objects.get(id=request.session['item_id_added'])
			except Exception, e:
				ctx = {"message":"Create an item shop, before upload images","title":"Can't upload images"}
				return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
			frm = expedient_item(item=item_instance,name=i,image=i)
		 	frm.save()
		try:
			del request.session['item_id_added']
		except Exception, e:
			pass
		
		return HttpResponseRedirect('/store/thanks_add_item/')
	else:
		frmExp = frmExpedient()
		ctx = {'frmExped':frmExp,'msg':""}
		return render_to_response('forms/store/add_expedient.html',ctx,context_instance=RequestContext(request))


@login_required
def thanks_add_item(request):
	return render_to_response('store/add_item_thanks.html',context_instance=RequestContext(request))


@login_required
def purchase_item(request):
	if request.method == "POST":
		item_purchase = int(request.POST['item'])
		_item = get_object_or_404(item, id=item_purchase)
		if _item.user == request.user:
			ctx = {'title':'This item belongs to you.','message':'This item belongs to you, you can not buy'}
			return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))
		frmPurchase = purchases(item=_item,user=request.user)
		frmPurchase.save()
		paypal = {
		'amount':frmPurchase.item.price,
		'item_name': frmPurchase.item.title,
		'item_number': frmPurchase.item.id,
		# PayPal wants a unique invoice ID
		'invoice': str(uuid.uuid1()),
		# It'll be a good idea to setup a SITE_DOMAIN inside settings
		# so you don't need to hardcode these values.
		'return_url': settings.SITE_DOMAIN + reverse('return_url'),
		'cancel_return': settings.SITE_DOMAIN + reverse('cancel_url'),
		}
		form = PayPalPaymentsForm(initial=paypal)
		if settings.DEBUG:
			rendered_form = form.sandbox()
		else:
			rendered_form = form.render()
		ctx = {'item' : _item,'form' : rendered_form,}
		return render_to_response('store/purchase_thanks.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/store/')


@login_required
def pay_item(request,idItem):
	idIt = idItem
	_item 	= get_object_or_404(item,id=idIt)
	_purch	= get_object_or_404(purchases,item=_item)
	if _purch.user == request.user:
		paypal = {
		'amount':_purch.item.price,
		'item_name': _purch.item.title,
		'item_number': _purch.item.id,
		# PayPal wants a unique invoice ID
		'invoice': str(uuid.uuid1()),
		# It'll be a good idea to setup a SITE_DOMAIN inside settings
		# so you don't need to hardcode these values.
		'return_url': settings.SITE_DOMAIN + reverse('return_url'),
		'cancel_return': settings.SITE_DOMAIN + reverse('cancel_url'),
		}
		form = PayPalPaymentsForm(initial=paypal)
		if settings.DEBUG:
			rendered_form = form.sandbox()
		else:
			rendered_form = form.render()
		ctx = {'item' : _item,'form' : rendered_form,}
		return render_to_response('store/purchase_thanks.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/profile/purchased/images/')


@login_required
def download_expedient(request,idItem):
	idIt = idItem
	item_instance = get_object_or_404(item,id=idIt)
	item_pur = get_object_or_404(purchases,item=item_instance)
	downloads(user=request.user,item_purchased=item_pur).save()
	if item_pur.user == request.user:
		import os, tempfile, zipfile
		from django.core.servers.basehttp import FileWrapper
		""" Make zip and download """
		temp = tempfile.TemporaryFile()
		archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
		item_expedient = expedient_item.objects.filter(item=item_instance)
		for i in item_expedient:
			filename = "%s/%s" % (settings.MEDIA_ROOT,  i.image)
			archive.write(filename,"%s" % i.name)
		archive.close()
		wrapper = FileWrapper(temp)
		response = HttpResponse(wrapper,content_type='application/zip')
		response['Content-Disposition'] = 'attachment: filename=download.zip'
		response['Content-Length'] = temp.tell()
		temp.seek(0)
		print "fin"
		return response	
	else:
		ctx = {"title":"You have not purchased this item","message":"Buy this image to download please"}
		return render_to_response("message/message.html",ctx,context_instance=RequestContext(request))
	

@login_required
def liberate_item(request,idItem):
	idItem = int(idItem)
	objItem = get_object_or_404(item,pk=idItem)
	objPurchase = get_object_or_404(purchases,item=objItem)
	if objPurchase.user == request.user:
		objPurchase.released = True
		objPurchase.save()
		return HttpResponseRedirect('/profile/purchased/images/')
	else:
		ctx = {'title':"Message",'message':"<h4>You do not have permission to do this</h4> <p>Return to <a href='/store/'>Store</a></p>"}
		return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))


	

def return_url_fn(request):
	print "test"

def cancel_url_fn(request):
	print "test"


@login_required
def edit_item(request,idImg):
	if request.method == "POST":
		idItem = int(request.POST['idItem'])
		item_instance = get_object_or_404(item,id=idItem)
		if item_instance.user != request.user:
			ctx ={'title':"You can't edit this item",'message':"You are not the owner of the image"}
			return render_to_response("message/message.html",ctx,context_instance=RequestContext(request))
		frmImage = add_item_store(request.POST,request.FILES,instance=item_instance)
		if frmImage.is_valid() :
			frmImage.save()
			ctx = {'objForm':frmImage,'msg':"Information stored successfully"}
			return render_to_response('forms/store/add_item_store.html',ctx,context_instance=RequestContext(request))
		
	idI = int(idImg)
	item_instance = get_object_or_404(item,id=idI)
	frmImage = add_item_store(instance=item_instance)
	ctx = {'objForm':frmImage,'msg':"",'idItem':idI}
	return render_to_response('forms/store/add_item_store.html',ctx,context_instance=RequestContext(request))


@login_required
def delete_item(request,idImg):
	idI = int(idImg)
	item_instance = get_object_or_404(item,id=idI)
	if item_instance.user == request.user:
		item_instance.delete()
		expedient_item.objects.filter(item=item_instance).delete()
		return HttpResponseRedirect('/profile/store/')
	else:
		ctx = {'title':'You can not erase this item','message':'This item does not belong'}
		return render_to_response('message/message.html',ctx,context_instance=RequestContext(request))


