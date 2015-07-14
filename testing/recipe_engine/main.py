from testing.recipe_engine.scraper import Recipe
from testing.recipe_engine.db_link import save_recipe

def retrieve_recipes():
    with open("urls.txt", 'r') as f:
        urls = f.readlines();
        for url in urls:
            url = url.strip('\n')
            recipe = Recipe(url)
            print("Saving %s" % recipe.title)
            save_recipe(recipe)
