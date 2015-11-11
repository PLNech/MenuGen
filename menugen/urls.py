from django.conf.urls import patterns, include, url
from django.contrib import admin
from menugen import settings
from rest_framework import routers
from menus.views import views
from django.views.generic import TemplateView

admin.site.site_header = 'Menugen - Administration'
admin.autodiscover()

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'recipetoingredients', views.RecipeToIngredientViewSet)
router.register(r'recipes', views.RecipeViewSet, base_name="recipe")
router.register(r'diets', views.DietViewSet)
router.register(r'ingredients', views.IngredientViewSet, base_name="ingredient")
router.register(r'ingredientnutriments', views.IngredientNutrimentViewSet)
router.register(r'ingredientfamilies', views.IngredientFamilyViewSet)
router.register(r'nutriments', views.NutrimentViewSet)
router.register(r'menus', views.MenuViewSet)
router.register(r'meals', views.MealViewSet)

urlpatterns = patterns(
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),

    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

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
