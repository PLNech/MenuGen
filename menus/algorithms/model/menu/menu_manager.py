import inspect
import time

__author__ = 'PLNech'

from random import randrange
import threading

from utils.printer import Printer
from menus.algorithms.model.manager import Manager
from menus.algorithms.model.menu.dish import Dish
from utils.config import Config

_local = threading.local()


class MenuManager(Manager):

    @staticmethod
    def get():
        caller = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
        if 'MenuManager' not in _local.__dict__:
            print(Printer.err("MenuManager not found. initialising cache procedure..."))
            _local.MenuManager = MenuManager()
            _local.MenuManager.init()
            items = _local.MenuManager.count()

            # print("Caching MenuManager with %d items          <%s.%s object at %s> [%s]" % (
            #     items,
            #     _local.MenuManager.__class__.__module__,
            #     _local.MenuManager.__class__.__name__,
            #     hex(id(_local.MenuManager)),
            #     caller))
            print(_local.MenuManager.print_items())
        else:
            items = _local.MenuManager.count()
            # print("Returning cached MenuManager with %d items <%s.%s object at %s> [%s]" % (
            #     items,
            #     _local.MenuManager.__class__.__module__,
            #     _local.MenuManager.__class__.__name__,
            #     hex(id(_local.MenuManager)),
            #     caller))

        return _local.MenuManager

    def __init__(self):
        self.dishes = []
        self.names_count = {}

    def init(self):
        nb_dishes = Config.parameters[Config.KEY_NB_DISHES]
        self.reset()
        for i in range(nb_dishes):
            dish = Dish()
            gen_name = dish.name
            if gen_name in self.names_count:
                self.names_count[gen_name] += 1
                dish.name += "(%d)" % self.names_count[gen_name]
            else:
                self.names_count[gen_name] = 1
            # dish.name = dish.name + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
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
            msg = "%s was not found in MenuManager:\n%s." % (str(dish), self.print_items())
            print(msg, flush=True)
            raise ValueError(msg)

    def print_items(self):
        return "\n".join(map(str, self.dishes))

    def count(self):
        return len(self.dishes)
