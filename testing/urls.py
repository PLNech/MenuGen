from django.conf.urls import patterns, url

urlpatterns = patterns(
    'testing.views',
    url(r'^testing$', 'index'),
    url(r'^testing/recipes$', 'recipes'),
)
