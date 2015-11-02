from django.conf.urls import patterns, url

urlpatterns = patterns(
    'application.views',
    url(r'^$', 'app')
)
