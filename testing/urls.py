from django.conf.urls import patterns, url

urlpatterns = patterns(
    'testing.views',
    url(r'^testing$', 'dashboard'),
    url(r'^testing/recipes$', 'recipes_default'),
    url(r'^testing/recipes/([0-9]+)$', 'recipes'),
    url(r'^testing/dashboard$', 'dashboard'),
    url(r'^testing/dashboard/ingredients$', 'dashboard_ingreds'),
    url(r'^testing/recipe_details/([0-9]+)$', 'recipe_details', name='recipe_details'),
    url(r'^testing/recipe_details_marmiton$', 'recipe_details_marmiton', name='recipe_details_marmiton'),
)
