from django.conf.urls.defaults import patterns, include, url

from carpooling.system.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'carpooling.views.home', name='home'),
    # url(r'^carpooling/', include('carpooling.foo.urls')),

    url(r'^login$', LoginScreen.as_view(), name="login"),
    #url(r'^logged$', LoggedScreen.as_view(), name="logged"),
    url(r'^schedule$', ScheduleScreen.as_view(), name="schedule"),
    url(r'^registration$', RegistrationScreen.as_view(), name="registration"),
    url(r'^administrate$', AdministrateScreen.as_view(), name="administrate"),
    url(r'^matchings$', MatchingScreen.as_view(), name="matchings"),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    
)
