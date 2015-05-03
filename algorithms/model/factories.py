__author__ = 'PLNech'

from model.trip.city import City
from model.trip.trip import Trip
from model.menu.menu import Menu
from model.menu.dish import Dish
from model.trip.trip_manager import TripManager
from model.menu.menu_manager import MenuManager
from utils.config import Config


class Factory:
    individual_types = {
        "Trip": Trip,
        "Menu": Menu,
    }

    gene_types = {
        "Trip": City,
        "Menu": Dish,
    }

    manager_types = {
        "Trip": TripManager,
        "Menu": MenuManager,
    }

    @staticmethod
    def individual(args=None, type_name=Config.parameters[Config.KEY_SOLUTION_TYPE]):
        """
        Factory method to create specialised individuals
        :type type_name str
        :except ValueError if the given type is not recognised
        :return: An Individual of the requested type
        :rtype Individual
        """
        if type_name in Factory.individual_types:
            constructor = Factory.individual_types[type_name]
            if args is not None:
                return constructor(args)
            else:
                return constructor()
        else:
            raise ValueError("%s is not an implemented individual type." % type_name)

    @staticmethod
    def gene(args=None, type_name=Config.parameters[Config.KEY_SOLUTION_TYPE]):
        """
        Factory method to get random genes
        :type type_name str
        :except ValueError if the given type is not recognised
        :return: A random Gene of the requested type
        """
        if type_name is "Menu":
            return MenuManager.get_random()

        elif type_name in Factory.individual_types:
            constructor = Factory.gene_types[type_name]
            if args is not None:
                return constructor(args)
            else:
                return constructor()
        else:
            raise ValueError("%s is not an implemented individual type." % type_name)


    @staticmethod
    def manager(args=None, type_name=Config.parameters[Config.KEY_SOLUTION_TYPE]):
        """
        Factory method to create gene managers
        :type type_name str
        :except ValueError if the given type is not recognised
        :return: A Manager of the requested type
        """
        if type_name in Factory.manager_types:
            constructor = Factory.manager_types[type_name]
            if args is not None:
                return constructor(args)
            else:
                return constructor()
        else:
            raise ValueError("%s is not an implemented individual type." % type_name)


def choose_method(trip_method, menu_method, args, type_name=Config.parameters[Config.KEY_SOLUTION_TYPE]):
    """
    Switch to choose the appropriate method by run type
    :param trip_method: Method to run if we are handling Trips and Cities
    :param menu_method: Method to run if we are handling Menus and Dishes
    :param args: arguments to pass on to the called method
    :param type_name: name of the type to lookup, defaulted to current solution type
    :return: the return value of the called method
    """
    if type_name is "Trip":
        if args is None:
            ret = trip_method()
        elif not isinstance(args, (frozenset, list, set, tuple,)):
            ret = trip_method(args)
        else:
            ret = trip_method(*args)
    elif type_name is "Menu":
        if args is None:
            ret = menu_method()
        elif not isinstance(args, (frozenset, list, set, tuple,)):
            ret = menu_method(args)
        else:
            ret = menu_method(*args)
    else:
        raise ValueError("%s is not an implemented type." % type_name)
    return ret


def is_better_than(score, old_score, type_name=Config.parameters[Config.KEY_SOLUTION_TYPE]):
    if type_name is "Trip":
        return score < old_score
    elif type_name is "Menu":
        return score > old_score
    else:
        raise ValueError("%s is not an implemented type." % type_name)
