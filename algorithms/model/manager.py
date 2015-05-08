__author__ = 'PLNech'

from utils.singleton import singleton


class Manager(singleton):

    def __str__(self):
        return Manager.print_items(self)

    def init(self):
        """
        Initialises the manager with random items

        """
        raise NotImplementedError()

    def reset(self):
        """
        Resets the manager, emptying its item list
        :return:
        """
        raise NotImplementedError()

    def add_item(self, item):
        """
        Adds an item to the manager's list

        :param item
        :type item object
        """
        raise NotImplementedError()

    def get_item(self, index):
        """
        Get the item at the given index

        :param index
        :type index int
        :return: the item
        """
        raise NotImplementedError()

    def get_index(self, item):
        """
        Get the index of a given item
        :param item: The item to lookup
        :rtype int
        :raises ValueError if the manager does not have this item
        """
        raise NotImplementedError()

    def print_items(self):
        """
        Prints the items currently in the manager

        """
        raise NotImplementedError()

    def count(self):
        """
        Returns the amount of items in the manager
        :rtype int
        """
        raise NotImplementedError()
