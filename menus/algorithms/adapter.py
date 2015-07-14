from menus.models import Recipe, IngredientNutriment, Nutriment
from .model.menu.dish import Dish

__author__ = 'PLNech'


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
    for ingredient in recipe.ingredients.all():
        nutriments = IngredientNutriment.objects
        # ing_cal = nutriments.get(ingredient=ingredient, nutriment=Nutriment.objects.get(name="\u00C9nergie")).quantity
        # ing_prot = nutriments.get(ingredient=ingredient, nutriment=Nutriment.objects.get(name="Prot")).quantity
        # ing_fat = nutriments.get(ingredient=ingredient, nutriment=Nutriment.objects.get(name="Lipides")).quantity
        # ing_carb = nutriments.get(ingredient=ingredient, nutriment=Nutriment.objects.get(name="Glucides")).quantity
        print("Ingredient %s: %f cal, %f prot, %f fat, %f carb." % (dish.name, ing_cal, ing_prot, ing_fat, ing_carb))
