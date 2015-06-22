from menus.models import Recipe, Ingredient

def get_matching_ingredient(parsed_ingredient):
    matching = Ingredient.objects.filter(name=parsed_ingredient)
    if not matching:
        matching = Ingredient.objects.filter(name__icontains=parsed_ingredient)
    return matching[0] if matching else None

def get_ease(parsed_ease):
    ease = {
        "très facile": 0,
        "facile": 1,
        "moyenne": 2,
        "difficile": 3
    }
    try:
        return ease[parsed_ease]
    except KeyError:
        if "facile" in parsed_ease:
            return 0
        if "moyen" in parsed_ease:
            return 2
        if "difficile" in parsed_ease:
            return 3
        return 2

def save_recipe(recipe):
    """
    :param recipe:the recipe scraped from marmiton
    :return: the ingredients matched
    """
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
    r.difficulty = get_ease(recipe.difficulty.lower())
    r.price = price[recipe.price_range.lower()]
    r.steps = recipe.instructions
    r.detail = recipe.remarks
    r.drink = recipe.drink
    r.origin_url = recipe.url
    r.save()

    # Link with ingredients
    # attempts in order:
    #   perfect match
    #   containing the string
    #   above steps with every word in the string from longest to shortest
    matched_ingredients = {}
    for i in recipe.ingredients:
        ingredient = get_matching_ingredient(i.name)
        if not ingredient:
            print(i.name)
            print("------")
            for word in reversed(sorted(i.name.split(" "), key=len)):
                print(word)
                ingredient = get_matching_ingredient(word)
                if ingredient:
                    break
        if ingredient:
            r.ingredients.add(ingredient)
            matched_ingredients[i.name] = ingredient.name
        else:
            matched_ingredients[i.name] = "[Not found]"

    return matched_ingredients
