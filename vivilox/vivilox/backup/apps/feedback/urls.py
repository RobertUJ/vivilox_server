from django.conf.urls.defaults import patterns,url
urlpatterns = patterns('vivilox.apps.feedback.views',
	url(r'^profile/feedback/$','view_feedback',name='feedback_view'),
	url(r'^profile/feedback/new/(\d{1,6})/(\d{1,6})/(\d{1,6})/(\d{1,6})/$','feedback_add',name='feedback_add'),
	url(r'^profile/feedback/delete/(\d{1,6})/$','feedback_delete',name='feedback_delete_view'),
)