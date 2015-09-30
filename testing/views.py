from django.shortcuts import render
from django.conf import settings

import testing.recipe_engine.scraper
from testing.recipe_engine.db_link import get_matching_ingredients, save_recipe
from menus.models import Recipe, RecipeToIngredient, Ingredient, Nutriment
from testing.recipe_engine.main import retrieve_recipes

def index(request):
    return render(request, 'index.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {
        'nb_recipes': Recipe.objects.count(),
        'nb_ingreds': Ingredient.objects.count(),
        'nb_nut': Nutriment.objects.count(),
        'nb_very_easy': Recipe.objects.filter(difficulty=0).count(),
        'nb_easy': Recipe.objects.filter(difficulty=1).count(),
        'nb_medium': Recipe.objects.filter(difficulty=2).count(),
        'nb_difficult': Recipe.objects.filter(difficulty=3).count(),
        'amount_1': Recipe.objects.filter(amount=1).count(),
        'amount_2':  Recipe.objects.filter(amount=2).count(),
        'amount_3': Recipe.objects.filter(amount=3).count(),
        'amount_4': Recipe.objects.filter(amount=4).count(),
        'amount_many': Recipe.objects.filter(amount__gte=5).count(),
        'price_0': Recipe.objects.filter(price=0).count(),
        'price_1': Recipe.objects.filter(price=1).count(),
        'price_2': Recipe.objects.filter(price=2).count(),
        'cat_amuse_gueule': Recipe.objects.filter(category='Amuse-gueule').count(),
        'cat_confiserie': Recipe.objects.filter(category='Confiserie').count(),
        'cat_conseil': Recipe.objects.filter(category='Conseil').count(),
        'cat_accompagnement': Recipe.objects.filter(category='Accompagnement').count(),
        'cat_dessert': Recipe.objects.filter(category='Dessert').count(),
        'cat_entree': Recipe.objects.filter(category='Entrée').count(),
        'cat_sauce': Recipe.objects.filter(category='Sauce').count(),
        'cat_boisson': Recipe.objects.filter(category='Boisson').count(),
        'cat_plat_principal': Recipe.objects.filter(category='Plat principal').count(),
    })

def recipes(request):
    # todo: show all recipe and paginate
    recipes = Recipe.objects.all()[:50]
    return render(request, 'recipes.html', {
        'recipes': recipes
    })

def recipe_details(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_to_ingredient = RecipeToIngredient.objects.filter(recipe=recipe)
    return render(request, 'recipe_details.html', {
        'recipe': recipe,
        'recipe_to_ingredient': recipe_to_ingredient
    })

def recipe_details_marmiton(request):
    if 'recipe_url' in request.POST and request.POST['recipe_url']:
        recipe = testing.recipe_engine.scraper.Recipe(request.POST['recipe_url'])
        if 'save' in request.POST and request.POST['save']:
            save_recipe(recipe)
    else:
        recipe = testing.recipe_engine.scraper.random_recipe()
    recipe.save_screenshot()
    screenshot = settings.MEDIA_ROOT + '/screen.jpg'
    matched_ingredients = get_matching_ingredients(recipe.ingredients)

    return render(request, 'recipe_details_marmiton.html', {
        'recipe': recipe,
        'screenshot': screenshot,
        'matched_ingredients': matched_ingredients,
    })

