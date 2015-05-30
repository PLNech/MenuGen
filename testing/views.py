from django.shortcuts import render
from testing.recipe_engine.scraper import random_recipe

def index(request):
    return render(request, 'index.html', {})

def recipes(request):
    recipe = random_recipe()
    recipe.save_screenshot()
    return render(request, 'recipes.html', { 'recipe': recipe })
