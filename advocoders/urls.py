from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'advocoders.views.home', name='home'),
    url(r'^company/(?P<domain>([^/]*))$', 'advocoders.views.home', name='home'),
    url(r'^logout$', 'advocoders.views.logout', name='logout'),
    url(r'^profile$', 'advocoders.views.profile', name='profile'),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
