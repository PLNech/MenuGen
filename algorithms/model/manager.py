__author__ = 'PLNech'

from utils.singleton import Singleton


class Manager(Singleton):

    def __str__(self):
        return Manager.print_items()

    @staticmethod
    def init():
        """
        Initialises the manager with random items

        """
        raise NotImplementedError()

    @staticmethod
    def reset():
        """
        Resets the manager, emptying its item list
        :return:
        """
        raise NotImplementedError()

    @staticmethod
    def add_item(item):
        """
        Adds an item to the manager's list

        :param item
        :type item object
        """
        raise NotImplementedError()

    @staticmethod
    def get_item(index):
        """
        Get the item at the given index

        :param index
        :type index int
        :return: the item
        """
        raise NotImplementedError()

    @staticmethod
    def get_index(item):
        """
        Get the index of a given item
        :param item: The item to lookup
        :rtype int
        :raises ValueError if the manager does not have this item
        """
        raise NotImplementedError()

    @staticmethod
    def print_items():
        """
        Prints the items currently in the manager

        """
        raise NotImplementedError()

    @staticmethod
    def count():
        """
        Returns the amount of items in the manager
        :rtype int
        """
        raise NotImplementedError()
