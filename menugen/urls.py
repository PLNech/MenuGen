from django.conf.urls import patterns, include, url
from django.contrib import admin
from menugen import settings

admin.site.site_header = 'Menugen - Administration'
admin.autodiscover()

urlpatterns = patterns(
    url(r'^', include('application.urls')),
    url(r'^', include('menus.urls')),
    url(r'^', include('testing.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
