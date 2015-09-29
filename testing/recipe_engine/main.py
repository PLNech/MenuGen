from testing.recipe_engine.scraper import Recipe
from testing.recipe_engine.db_link import save_recipe
import menus.models
import time

def retrieve_recipes():
    with open("testing/recipe_engine/good_recipes.txt", 'r') as f:
        urls = f.readlines();
        for i, url in enumerate(urls):
            url = url.strip('\n')
            recipe = Recipe(url)
            if not menus.models.Recipe.objects.filter(name=recipe.title):
                try:
                    save_recipe(recipe)
                except:
                    break
                print("Saved %s" % recipe.title)
            else:
                print("Skipping %s, already in database" % recipe.title)
            if i % 1000 == 0:
                time.sleep(600)
