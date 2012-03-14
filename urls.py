from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template, redirect_to


admin.autodiscover()

urlpatterns = patterns('',
    
    # Apps
    url(r'^admin/', include(admin.site.urls)),

    #Very basic forms for demo purposes only.
    url(r'^logout/', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'transit_subsidy/login.html'}, name='login'),
   
    #Replace with you're index view
    url(r'^$', redirect_to, {'url': '/transit'}),

    # Smartrip Transit Subsidy
    url(r'transit/$','transit_subsidy.views.home'),
    url(r'transit/csv$','transit_subsidy.views.dump_csv'), 
    url(r'transit/modes$','transit_subsidy.views.modes_json'), 
    url(r'transit/cancel$','transit_subsidy.views.cancel'),
    url(r'transit/approve$','transit_subsidy.views.approve'),
    url(r'transit/json$','transit_subsidy.views.approval_json'), 
    url(r'transit/approve_transit$','transit_subsidy.views.approve_transit'), 
    
)
# urlpatterns += staticfiles_urlpatterns()
