import unicodedata
from menus.algorithms.utils.printer import Printer
from menus.models import Recipe, IngredientNutriment, Nutriment, RecipeToIngredient
from .model.menu.dish import Dish
import unidecode

__author__ = 'PLNech'


def dish2recipe(dish):
    """
    :type dish Dish
    :rtype: Recipe
    """
    recipe = Recipe.objects.get(pk=dish.recipe_id)
    return recipe


def recipe2dish(recipe, verbose=1):
    """
    :type recipe Recipe
    :return: Dish
    """

    dish = Dish(recipe.name, recipe.id)

    if verbose > 0:
        print("\n------------\nHandling recipe: %s." % dish.name)
    nuts = IngredientNutriment.objects
    for ing in recipe.ingredients.all():
        association = RecipeToIngredient.objects.filter(recipe=recipe, ingredient=ing)[0]
        if verbose > 1:
            print("%s %s of %s." % (association.quantity, association.unit, ing.name))

        ing_cal = calculate_nutrients(association, nuts, "Energie, R\u00E8glement UE N\u00B0 1169/2011", 'kcal')
        ing_prot = calculate_nutrients(association, nuts, "Prot\u00E9ines")
        ing_fat = calculate_nutrients(association, nuts, "Lipides")
        ing_carb = calculate_nutrients(association, nuts, "Glucides")
        if verbose > 1:
            print("Ingredient %s: %f cal, %f prot, %f fat, %f carb." %
                  (ing.name, ing_cal, ing_prot, ing_fat, ing_carb))
        ingredient_dish = Dish(name=ing.name,
                               calories=ing_cal, proteins=ing_prot, fats=ing_fat, carbohydrates=ing_carb)
        dish += ingredient_dish
    if verbose > 0:
        print("Nutrients: %f cal, %f prot, %f fat, %f carb.\n------------\n" %
              (dish.calories, dish.proteins, dish.fats, dish.carbohydrates))
    return dish


def calculate_nutrients(association, nuts, name, unit=None):
    if association.quantity is None or association.quantity is 0:
        association.quantity = 1

    coeff_dict = {
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

    if unit is not None:
        nutriment = Nutriment.objects.get(name=name, unit_per_100g=unit)
    else:
        nutriment = Nutriment.objects.get(name=name)

    ascii_unit = None if association.unit is None else unidecode.unidecode(association.unit)

    link = nuts.get(ingredient=association.ingredient, nutriment=nutriment)

    if ascii_unit in coeff_dict:
        coeff = coeff_dict[ascii_unit]
    else:
        print(Printer.err("The following unit could not be quantified: %s." % ascii_unit))
        coeff = 1
    return coeff * link.quantity * association.quantity / association.recipe.amount
