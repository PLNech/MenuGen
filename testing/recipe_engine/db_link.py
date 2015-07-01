from menus.models import Recipe, Ingredient
from Levenshtein import distance
import testing.models

def get_closest(parsed_ingredient, matching):
    """
    :param parsed_ingredient:
    :param matching: matching ingredients
    :return: the closest matching using Levenshtein's distance
    """
    scores = {}
    for m in matching:
        scores[distance(parsed_ingredient, m.name)] = m
    return scores[sorted(scores.keys())[0]]


def get_matching_ingredient(parsed_ingredient, ciqual=False):
    if not parsed_ingredient:
        return None
    if ciqual:
        matching = testing.models.Ingredient.objects.filter(name=parsed_ingredient)
    else:
        matching = Ingredient.objects.filter(name=parsed_ingredient)
    if not matching and parsed_ingredient.endswith('s'):
        if ciqual:
            matching = testing.models.Ingredient.objects.filter(name=parsed_ingredient[:-1])
        else:
            matching = Ingredient.objects.filter(name=parsed_ingredient[:-1])
    if not matching:
        if not matching and parsed_ingredient.endswith('s'):
            if ciqual:
                matching = testing.models.Ingredient.objects.filter(name__icontains=parsed_ingredient[:-1])
            else:
                matching = Ingredient.objects.filter(name__icontains=parsed_ingredient[:-1])
        if not matching:
            if ciqual:
                matching = testing.models.Ingredient.objects.filter(name__icontains=parsed_ingredient)
            else:
                matching = Ingredient.objects.filter(name__icontains=parsed_ingredient)
    return get_closest(parsed_ingredient, matching) if matching else None

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

def get_matching_ingredients(parsed_ingredients, recipe=None):
    """
    :param parsed_ingredients: the ingredients parsed from a marmiton recipe
    :param recipe: the recipe to link to the ingredients
    :return:matching ingredients from the database
    """
    # attempts in order:
    #   perfect match
    #   containing the string
    #   above steps with every word in the string from longest to shortest
    matched_ingredients = {}
    for i in parsed_ingredients:
        if not i or not i.name:
            continue
        ingredient = get_matching_ingredient(i.name)
        if not ingredient:
            for word in reversed(sorted(i.name.split(" "), key=len)):
                ingredient = get_matching_ingredient(word)
                if ingredient:
                    break

        if ingredient:
            if recipe:
                recipe.ingredients.add(ingredient)
            matched_ingredients[i.name] = ingredient.name
        else:
            matched_ingredients[i.name] = "<None>"

    return matched_ingredients

def get_matching_ciqual_ingredients(parsed_ingredients):
    matched_ingredients = {}
    for i in parsed_ingredients:
        if not i:
            continue
        ingredient = get_matching_ingredient(i.name, True)
        if not ingredient:
            for word in reversed(sorted(i.name.split(" "), key=len)):
                ingredient = get_matching_ingredient(word, True)
                if ingredient:
                    break

        if ingredient:
            matched_ingredients[i.name] = ingredient.name
        else:
            matched_ingredients[i.name] = "<None>"

    return matched_ingredients

def link_ingredients(recipe, ingredients):
    get_matching_ingredients(ingredients, recipe)

def save_recipe(recipe):
    """
    Save the recipe into the database
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

    link_ingredients(r, recipe.ingredients)

