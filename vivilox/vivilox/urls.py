from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vivilox.views.home', name='home'),
    # url(r'^vivilox/', include('vivilox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login'),

    #Import urls.py's apps 
    url(r'^',include('vivilox.apps.home.urls')),
    url(r'^',include('vivilox.apps.contests.urls')),
    url(r'^',include('vivilox.apps.store.urls')),
    url(r'^',include('vivilox.apps.accounts.urls')),
    url(r'^',include('vivilox.apps.feedback.urls')),
    url(r'^something-hard-to-guess/', include('paypal.standard.ipn.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT}),
)
