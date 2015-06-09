__author__ = 'PLNech'

from utils.comparable import Comparable


class Individual(Comparable):
    def __init__(self):
        self.genes = []
        raise NotImplementedError("Individual is an abstract class.")

    def get_score(self):
        """
        Get total score of the individual's solution

        :rtype: int
        """
        raise NotImplementedError()

    def print_score(self):
        """
        Get total score of the individual's solution as a string

        :rtype: str
        """
        raise NotImplementedError()

    def print_fitness(self):
        """
        Get total score of the individual's solution as a detailed string

        :rtype: str
        """
        raise NotImplementedError()

    def get_fitness(self):
        """
        Get the fitness of the individual's solution

        :rtype: float
        """
        raise NotImplementedError()

    def genome_length(self):
        """
        Get total length of the individual's genome

        :rtype: int
        """
        raise NotImplementedError()

    def get_gene(self, index):  # TODO Generic return type
        """
        Get the gene at the given index of the individual's genome

        :rtype Trip
        """
        raise NotImplementedError()

    def set_gene(self, index, gene):
        """
        Set the gene at given index with given value

        :param index:
        :param gene:
        """
        raise NotImplementedError()

    def generate(self):
        """
        Generates the genome with random values

        """
        raise NotImplementedError()

    def print_short(self):
        """
        Prints a short string identifying the individual

        :rtype str
        """
        raise NotImplementedError()
