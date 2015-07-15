from django.shortcuts import render
from django.conf import settings

from testing.models import Comment
from testing.recipe_engine.scraper import random_recipe, Recipe
from testing.recipe_engine.db_link import get_matching_ingredients, save_recipe
from testing.recipe_engine.main import retrieve_recipes

def index(request):
    return render(request, 'index.html', {})

def recipes(request):
    if 'recipe_url' in request.POST and request.POST['recipe_url']:
        recipe = Recipe(request.POST['recipe_url'])
        if 'save' in request.POST and request.POST['save']:
            #save_recipe(recipe)
            retrieve_recipes()
    else:
        recipe = random_recipe()
    #recipe.save_screenshot()
    screenshot = settings.MEDIA_ROOT + '/screen.jpg'
    matched_ingredients = get_matching_ingredients(recipe.ingredients)

    com_saved = False
    if 'new_comment' in request.POST and request.POST['new_comment']:
        if 'com_url' in request.POST and request.POST['com_url']:
            com = Comment(url=request.POST['com_url'], text=request.POST['new_comment'])
            com.save()
            com_saved = True
    comments = Comment.objects.all()

    return render(request, 'recipes.html', {
        'recipe': recipe,
        'screenshot': screenshot,
        'matched_ingredients': matched_ingredients,
        'com_saved': com_saved,
        'comments': comments
    })

