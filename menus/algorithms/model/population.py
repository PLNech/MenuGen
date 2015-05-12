import os
from model.menu.menu import Menu
from model.menu.menu_manager import MenuManager

__author__ = 'PLNech'

from algorithms.model.individual import Individual
from utils.config import Config


class Population():
    def __init__(self, size=Config.parameters[Config.KEY_POPULATION_SIZE], initialise=True):

        """
        :param size:
        :param initialise:
        :return:
        :rtype Population
        """
        self.population = [None] * size
        manager = MenuManager()

        if initialise:
            if Config.print_population:
                print("Initialising population of size %i" % size)
            for i in range(size):
                new_individual = Menu()
                new_individual.generate()

                self.save_at(i, new_individual)
            if Config.print_population:
                print("Population generated: \n%s\n." % str(self))

    def __str__(self):
        pop_str = ""
        for i in range(self.get_size()):
            individual = self.get_at(i)
            if individual is None:
                individual = ""
            pop_str = pop_str + str(individual) + "\n"
        return pop_str

    def save_at(self, index, individual):
        """
        Saves an Individual at given index
        :type index int
        :type individual Individual
        """
        self.population[index] = individual

    def get_at(self, index):
        """
        Get the Individual at given index
        :type: index int

        :rtype: Individual
        """
        return self.population[index]

    def get_size(self):
        """

        :rtype: int
        """
        return len(self.population)

    def get_fittest(self):
        """
        Get the fittest Individual of the population
        :rtype: Individual
        """
        fittest = self.population[0]
        for i in range(self.get_size() - 1):
            individual_i = self.get_at(i)
            if fittest.get_fitness() <= individual_i.get_fitness():
                fittest = individual_i
        return fittest
