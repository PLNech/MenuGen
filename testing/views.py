from django.shortcuts import render
from django.conf import settings

from testing.recipe_engine.scraper import random_recipe, Recipe
from testing.recipe_engine.db_link import get_matching_ingredients, save_recipe

def index(request):
    return render(request, 'index.html', {})

def recipes(request):
    if 'recipe_url' in request.POST and request.POST['recipe_url']:
        recipe = Recipe(request.POST['recipe_url'])
        if 'save' in request.POST and request.POST['save']:
            save_recipe(recipe)
    else:
        recipe = random_recipe()
    recipe.save_screenshot()
    screenshot = settings.MEDIA_ROOT + '/screen.jpg'
    matched_ingredients = get_matching_ingredients(recipe.ingredients)

    return render(request, 'recipes.html', {
        'recipe': recipe,
        'screenshot': screenshot,
        'matched_ingredients': matched_ingredients,
    })

