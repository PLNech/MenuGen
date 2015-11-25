import logging
import unidecode
from menus.algorithms.model.menu.dish import Dish
from menus.models import Recipe, IngredientNutriment, Nutriment, RecipeToIngredient

__author__ = 'PLNech'
logger = logging.getLogger('menus')

recipe2ingredients_objects = RecipeToIngredient.objects
ingredient_nutriment_objects = IngredientNutriment.objects
nutriment_objects = Nutriment.objects

unit_coeff_dict = {
    'mg': 1 / 100000,
    'cg': 1 / 10000,
    'dg': 1 / 1000,
    'g': 1 / 100,
    'kg': 10,
    'ml': 1 / 100,
    'cl': 1 / 10,
    'l': 10,
    'cuillere a cafe': 1 / 20,
    'cuillere a soupe': 1 / 5.55,  # 18g en moyenne
    'verre': 1,  # 80g farine -> 120g sucre
    'gousse': 1 / 2.38,  # TODO: Could use ingredient ? Ail 7-12 -> oignon 100g...
    'tranche': 1 / 1.56,  # 23g pain blanc -> 140 minibaguette
    'boite': 1,
    'pot': 1.25,
    None: 1 / 5,  # No information -> 100g?  # TODO: Refine this by ingredient
}


def dish2recipe(dish):
    """
    :type dish Dish
    :rtype: Recipe
    """
    recipe = Recipe.objects.get(pk=dish.recipe_id)
    return recipe


def recipe2dish(recipe):
    """
    :type recipe Recipe
    :return: Dish
    """

    dish = Dish(recipe.name, recipe.id)

    logger.debug("Handling recipe: %s." % dish.name)
    for ing in recipe.ingredients.all():
        association = recipe2ingredients_objects.filter(recipe=recipe, ingredient=ing)[0]
        logger.debug("%s %s of %s.", association.quantity, association.unit, ing.name)

        ing_cal = calculate_nutrients(association, "Energie, R\u00E8glement UE N\u00B0 1169/2011", 'kcal')
        ing_prot = calculate_nutrients(association, "Prot\u00E9ines")
        ing_fat = calculate_nutrients(association, "Lipides")
        ing_carb = calculate_nutrients(association, "Glucides")
        logger.debug("Ingredient %s: %.3f cal, %.3f prot, %.3f fat, %.3f carb.",
                     ing.name, ing_cal, ing_prot, ing_fat, ing_carb)
        dish += Dish(name=ing.name, calories=ing_cal, proteins=ing_prot, fats=ing_fat, carbohydrates=ing_carb)
    logger.debug("Nutrients: %.3f cal, %.3f prot, %.3f fat, %.3f carb.\n------------", dish.calories, dish.proteins,
                 dish.fats, dish.carbohydrates)
    return dish


def calculate_nutrients(association, name, unit=None):
    if association.quantity is None or association.quantity is 0:
        association.quantity = 1

    if unit is not None:
        nutriment = nutriment_objects.get(name=name, unit_per_100g=unit)
    else:
        nutriment = nutriment_objects.get(name=name)
    link = ingredient_nutriment_objects.get(ingredient=association.ingredient, nutriment=nutriment)

    if association.unit is None:
        coeff = 1
    else:
        ascii_unit = unidecode.unidecode(association.unit)
        unit_lower = ascii_unit.lower()
        if unit_lower in unit_coeff_dict:
            coeff = unit_coeff_dict[unit_lower]
        else:
            logger.error("Could not quantify r:%s * i:%s (\"%s\"): %s." % (association.recipe.name,
                                                                           association.ingredient.name,
                                                                           association.scraped_text, ascii_unit))
            coeff = 1
    return coeff * link.quantity * association.quantity / association.recipe.amount
