from django.conf.urls.defaults import patterns,url
urlpatterns = patterns('vivilox.apps.accounts.views',
	url(r'^accounts/login/$','login_view',name='view_login'),
	url(r'^accounts/logout/$','logout_view',name='view_logout'),
	url(r'^accounts/new/$', 'register_user',name='new_user_view'),
	url(r'^profile/contest/$','profile_contest',name='profile_contest'),
	url(r'^profile/edit/$','edit_profile',name='edit_profile_view'),
	url(r'^profile/purchased/images/$','images_purchased',name="purchased_images_view"),
	url(r'^profile/store/$','my_store',name="my_store_view"),

)



	
