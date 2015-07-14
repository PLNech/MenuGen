import inspect
from menus.algorithms import adapter

from menus.models import Recipe

__author__ = 'PLNech'

from random import randrange, shuffle
import threading

from menus.algorithms.utils.printer import Printer
from menus.algorithms.model.manager import Manager
from menus.algorithms.model.menu.dish import Dish
from menus.algorithms.utils.config import Config

_local = threading.local()


class MenuManager(Manager):
    @staticmethod
    def get():
        caller = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
        if 'MenuManager' not in _local.__dict__:
            if Config.print_manager:
                print(Printer.err("MenuManager not found. initialising cache procedure..."))

            _local.MenuManager = MenuManager()
            _local.MenuManager.init()
            items = _local.MenuManager.count()

            if Config.print_manager:
                print("Caching MenuManager with %d items          <%s.%s object at %s> [%s]" % (
                    items,
                    _local.MenuManager.__class__.__module__,
                    _local.MenuManager.__class__.__name__,
                    hex(id(_local.MenuManager)),
                    caller))
                print(_local.MenuManager.print_items())
        elif Config.print_manager:
            items = _local.MenuManager.count()
            print("Returning cached MenuManager with %d items <%s.%s object at %s> [%s]" % (
                items,
                _local.MenuManager.__class__.__module__,
                _local.MenuManager.__class__.__name__,
                hex(id(_local.MenuManager)),
                caller))

        return _local.MenuManager

    def __init__(self):
        self.dishes = []
        self.names_count = {}

    def init(self):
        nb_dishes = Config.parameters[Config.KEY_NB_DISHES]
        self.reset()
        self.init_from_db(nb_dishes)
        if Config.print_manager:
            print("Initialised MenuManager with %i dishes." % len(self.dishes))

    def init_from_config(self, nb_dishes):
        for i in range(nb_dishes):
            dish = Dish()
            gen_name = dish.name

            if not self.add_item(dish):
                i -= 1
                continue

            if gen_name in self.names_count:
                self.names_count[gen_name] += 1
                dish.name += "(%d)" % self.names_count[gen_name]
            else:
                self.names_count[gen_name] = 1

            if Config.print_manager:
                print("Dish %s." % dish)

    def init_from_db(self, nb_dishes, profile=None):
        recipes = list(Recipe.objects.all()[:nb_dishes])
        shuffle(recipes)
        for i in range(nb_dishes):
            recipe = recipes[i]
            dish = adapter.recipe2dish(recipe)  # TODO: Link with nutritional information
            self.add_item(dish, profile)
            if Config.print_manager:
                print("Dish %s." % dish)

    def reset(self):
        self.dishes = []

    def add_item(self, dish, profile=None):
        if profile and not profile.likes(dish):
            return False
        else:
            self.dishes.append(dish)
            return True

    def get_item(self, index):
        return self.dishes[index]

    def get_random(self):
        nb_dishes = len(self.dishes)
        return self.dishes[randrange(0, nb_dishes)]

    def get_index(self, dish):
        try:
            return self.dishes.index(dish)
        except ValueError:
            msg = "%s was not found in MenuManager:\n%s." % (str(dish), self.print_items())
            if Config.print_manager:
                print(msg, flush=True)
            raise ValueError(msg)

    def print_items(self):
        return "\n".join(map(str, self.dishes))

    def count(self):
        return len(self.dishes)
