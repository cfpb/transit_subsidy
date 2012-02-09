from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template, redirect_to
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^logout/', 'front.views.logout_view', name='logout'),
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'transit_subsidy/login.html'}, name='login'),
   
    # Smartrip Transit Subsidy
    url(r'transit/$','transit_subsidy.views.home'),
    url(r'transit/csv$','transit_subsidy.views.dump_csv'), 
    url(r'transit/modes$','transit_subsidy.views.modes_json'), 
    
)
# urlpatterns += staticfiles_urlpatterns()
