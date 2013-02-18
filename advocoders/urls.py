from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import signals  # DO NOT REMOVE; register signals


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'advocoders.views.home', name='home'),
    url(r'^company/(?P<domain>([^/]*))$', 'advocoders.views.feed', name='feed_company'),
    url(r'^company/(?P<domain>([^/]*))/(?P<provider>([^/]*))$', 'advocoders.views.feed', name='feed_company_provider'),
    url(r'^my/company$', 'advocoders.views.my_company', name='my_company'),
    url(r'^logout$', 'advocoders.views.logout', name='logout'),
    url(r'^settings/profile$', 'advocoders.views.settings_profile', name='settings_profile'),
    url(r'^settings/feeds$', 'advocoders.views.settings_feeds', name='settings_feeds'),
    url(r'^settings/company$', 'advocoders.views.settings_company', name='settings_company'),
    url(r'', include('social_auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
