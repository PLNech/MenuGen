from menus.models import Recipe
from .model.menu.dish import Dish

__author__ = 'PLNech'


def dish_to_recipe(dish):
    """

    :param dish:
    :type dish Dish
    :rtype: Recipe
    """
    recipe = Recipe()
    recipe.name = dish.name
    return recipe
