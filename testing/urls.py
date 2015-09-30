from django.conf.urls import patterns, url

urlpatterns = patterns(
    'testing.views',
    url(r'^testing$', 'index'),
    url(r'^testing/recipes$', 'recipes'),
    url(r'^testing/recipe_details/([0-9]+)$', 'recipe_details', name='recipe_details'),
    url(r'^testing/recipe_details_marmiton$', 'recipe_details_marmiton', name='recipe_details_marmiton'),
)
