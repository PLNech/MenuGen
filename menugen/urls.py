from django.conf.urls import patterns, include, url
from django.contrib import admin
from menugen import settings
from rest_framework import routers
from menus.views import views

admin.site.site_header = 'Menugen - Administration'
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'recipetoingredients', views.RecipeToIngredientViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'diets', views.DietViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'ingredientnutriments', views.IngredientNutrimentViewSet)
router.register(r'ingredientfamilies', views.IngredientFamilyViewSet)
router.register(r'nutriments', views.NutrimentViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'meals', views.MealViewSet)

urlpatterns = patterns(
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    url(r'^', include('application.urls')),
    url(r'^', include('menus.urls')),
    url(r'^', include('testing.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
