from django.shortcuts import render
from django.conf import settings

import testing.recipe_engine.scraper
from testing.recipe_engine.db_link import get_matching_ingredients, save_recipe
from menus.models import Recipe, RecipeToIngredient

def index(request):
    return render(request, 'index.html', {})

def recipes(request):
    recipes = Recipe.objects.all()
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

