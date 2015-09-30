from testing.recipe_engine.scraper import Recipe
from testing.recipe_engine.db_link import save_recipe
import menus.models
import time

def retrieve_recipes():
    with open("testing/recipe_engine/good_recipes.txt", 'r') as f:
        urls = f.readlines();
        for i, url in enumerate(urls):
            url = url.strip('\n')
            try:
                recipe = Recipe(url)
                if not menus.models.Recipe.objects.filter(name=recipe.title):
                    save_recipe(recipe)
                    print("Saved %s (%s)" % (recipe.title, url))
                else:
                    print("Skipping %s, already in database" % recipe.title)
            except:
                continue
            if (i + 1) % 700 == 0:
                print("%s - Sleeping 15 minutes" % time.strftime("%H:%M"))
                time.sleep(900)
