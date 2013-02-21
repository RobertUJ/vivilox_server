from django.conf.urls.defaults import patterns,url

urlpatterns = patterns('vivilox.apps.store.views',
	url(r'^store/$','store',name='store_view'),
	url(r'^store.top/$','store_top',name='store_top_view'),
	url(r'^store/item/new/$','add_item',name='store_add_item_view'),
	url(r'^store/item/details/(\d{1,6})/$','image_details',name='image_details_view'),
	url(r'^store/item/purchase/$','purchase_item',name="item_purchase_view"),
	url(r'^store/item/edit/(\d{1,6})/$','edit_item',name="item_edit_view"),
	url(r'^store/item/delete/(\d{1,6})/$','delete_item',name="delete_item_view"),
	url(r'^store/expedient/new/$','add_item_expedient',name="add_item_expedient_view"),
	url(r'^store/thanks_add_item/$','thanks_add_item',name="thanks_add_item_view"),
	url(r'^store/download/expedient/(?P<idItem>\d{1,6})/$','download_expedient',name="download_expedient_view"),
	url(r'^store/pay/item/(?P<idItem>\d{1,6})/$','pay_item',name="pay_item_view"),
	url(r'^store/liberate/(\d{1,6})/$','liberate_item',name="liberate_item_view"),
	
	url(r'^store/return/$','return_url_fn',name="return_url"),
	url(r'^store/cancel/$','cancel_url_fn',name="cancel_url"),

	
	# /store/expedient/new/
)