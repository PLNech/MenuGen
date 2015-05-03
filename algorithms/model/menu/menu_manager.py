__author__ = 'PLNech'

from random import randrange
from collections import defaultdict

from model.manager import Manager
from model.menu.dish import Dish
from utils.config import Config


class MenuManager(Manager):
    dishes = []
    names_count = {}

    @staticmethod
    def init():
        for i in range(Config.parameters[Config.KEY_NB_DISHES]):
            dish = Dish()
            gen_name = dish.name
            if gen_name in MenuManager.names_count:
                MenuManager.names_count[gen_name] += 1
                dish.name += "(%d)" % MenuManager.names_count[gen_name]
            else:
                MenuManager.names_count[gen_name] = 1
            MenuManager.add_item(dish)

            if Config.print_items:
                print("Dish %s." % dish)

    @staticmethod
    def reset():
        MenuManager.dishes = []

    @staticmethod
    def add_item(dish):
        MenuManager.dishes.append(dish)

    @staticmethod
    def get_item(index):
        return MenuManager.dishes[index]

    @staticmethod
    def get_random():
        return MenuManager.dishes[randrange(0, len(MenuManager.dishes))]

    @staticmethod
    def get_index(dish):
        try:
            return MenuManager.dishes.index(dish)
        except ValueError:
            print("%s was not found in MenuManager:\n%s." % (str(dish), MenuManager.print_items()))
            raise ValueError()

    @staticmethod
    def print_items():
        return "\n".join(map(str, MenuManager.dishes))

    @staticmethod
    def count():
        return len(MenuManager.dishes)
