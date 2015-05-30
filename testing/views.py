from django.shortcuts import render
from testing.recipe_engine.scraper import random_recipe, Recipe

def index(request):
    return render(request, 'index.html', {})

def recipes(request):
    if 'recipe_url' in request.POST and request.POST['recipe_url']:
        recipe = Recipe(request.POST['recipe_url'])
    else:
        recipe = random_recipe()
    #recipe.save_screenshot()
    return render(request, 'recipes.html', { 'recipe': recipe })
