from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'advocoders.views.home', name='home'),
    url(r'^signup$', 'advocoders.views.signup', name='signup'),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
