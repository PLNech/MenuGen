from menus.models import Recipe, Ingredient

def get_matching_ingredient(parsed_ingredient):
    matching = Ingredient.objects.filter(name=parsed_ingredient)
    if not matching:
        matching = Ingredient.objects.filter(name__icontains=parsed_ingredient)
    return matching[0] if matching else None


def save_recipe(recipe):
    """
    :param recipe:the recipe scraped from marmiton
    """
    ease = {
        "très facile": 0,
        "facile": 1,
        "moyenne": 2,
        "difficile": 3
    }
    price = {
        "bon marché": 0,
        "moyen": 1,
        "assez cher": 2
    }
    r = Recipe()
    r.name = recipe.title
    r.picture = recipe.picture_url
    r.prep_time = recipe.preptime
    r.cook_time = recipe.cooktime
    r.amount = recipe.nb_person
    r.difficulty = ease[recipe.difficulty.lower()]
    r.price = price[recipe.price_range.lower()]
    r.steps = recipe.instructions
    r.detail = recipe.remarks
    r.drink = recipe.drink
    r.origin_url = recipe.url
    r.save()

    for i in recipe.ingredients:
        ingredient = get_matching_ingredient(i.name)
        if not ingredient:
            for word in i.name.split(" "):
                ingredient = get_matching_ingredient(word)
                if ingredient:
                    break
        if ingredient:
            r.ingredients.add(ingredient)
            print("%s => %s" %(i.name, ingredient.name))
        else:
            print("Ingredient not found: %" % i.name)
