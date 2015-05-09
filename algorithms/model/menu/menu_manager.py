__author__ = 'PLNech'

import os

from random import randrange

from algorithms.model.manager import Manager
from algorithms.model.menu.dish import Dish
from utils.config import Config


class MenuManager(Manager):
    dishes = []
    names_count = {}

    def __init__(self):
        if len(self.dishes) == 0:
            self.init()

    def init(self):
        for i in range(Config.parameters[Config.KEY_NB_DISHES]):
            dish = Dish()
            gen_name = dish.name
            if gen_name in self.names_count:
                self.names_count[gen_name] += 1
                dish.name += "(%d)" % self.names_count[gen_name]
            else:
                self.names_count[gen_name] = 1
            self.add_item(dish)

            if Config.print_items:
                print("Dish %s." % dish)
        print("Initialised MenuManager with %i dishes." % len(self.dishes))

    def reset(self):
        self.dishes = []

    def add_item(self, dish):
        self.dishes.append(dish)

    def get_item(self, index):
        return self.dishes[index]

    def get_random(self):
        nb_dishes = len(self.dishes)
        return self.dishes[randrange(0, nb_dishes)]

    def get_index(self, dish):
        try:
            return self.dishes.index(dish)
        except ValueError:
            print("%s was not found in MenuManager:\n%s." % (str(dish), self.print_items()))
            raise ValueError()

    def print_items(self):
        return "\n".join(map(str, self.dishes))

    def count(self):
        return len(self.dishes)
