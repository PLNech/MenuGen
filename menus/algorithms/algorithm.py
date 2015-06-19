from menus.algorithms.model.menu.menu import Menu
from menus.algorithms.model.menu.menu_manager import MenuManager

__author__ = 'PLNech'

import random
import math

from menus.algorithms.utils.config import Config
from menus.algorithms.utils.printer import Printer
from menus.algorithms.model.population import Population
from menus.algorithms.model.individual import Individual


def func_selection(population):
    """
    :type population Population
    :rtype Individual
    """
    individual = population.get_at(0)
    return individual


def func_crossover(parent1, parent2):
    """
    :type parent1 Individual
    :type parent2 Individual
    :rtype Individual
    """
    return parent2 if parent2 is None else parent1


def func_mutation(individual):
    """
    :type individual Individual
    :rtype Individual
    """
    return individual


def tournament_selection(population):
    """
    Tournament selection algorithm

    We run several "tournaments" among a few individuals chosen at random from the population ;
    the winner of each tournament is selected for crossover.

    Selection pressure is easily adjusted by changing the tournament size:
    larger tournament -> weak individuals have a smaller chance to be selected.

    :param population: The Population from which champions will be selected
    :return: The fittest individual of the tournament
    :type: population Population
    :rtype: Individual
    """
    # Create a tournament pool
    tournament = Population(Config.parameters[Config.KEY_TOURNAMENT_SIZE], False)

    for i in range(Config.parameters[Config.KEY_TOURNAMENT_SIZE]):
        random_id = random.randint(0, population.get_size() - 1)
        hero = population.get_at(random_id)
        tournament.save_at(i, hero)
        if Config.print_selection:
            print("Added hero %d to tournament: %s." % (i, hero.print_short()))
    # Return hero of tournament
    champion = tournament.get_fittest()
    if Config.print_selection:
        print("Champion of tournament: %s." % champion.print_short())
    return champion


def crossover_ordered(parent1, parent2):
    """
    Ordered crossover algorithm

    We randomly select a subset from our first parent and add it to our child.
    Finally we add the objects which are not yet in our child
    in the second parent's order.

    :param parent1: The first parent
    :param parent2: The second Parent
    :return: The newly created child
    :type parent1 Individual
    :type parent2 Individual
    """
    child = Menu()

    r1 = random.randint(0, parent1.genome_length())
    r2 = random.randint(0, parent1.genome_length())
    start_pos = min(r1, r2)
    end_pos = max(r1, r2)

    child_str = [""] * child.genome_length()
    for i in range(child.genome_length()):
        # If we are still before the end position, copy gene
        if start_pos < i < end_pos:
            child.set_gene(i, parent1.get_gene(i))
            child_str[i] = Printer.green("-")

    # Then loop through remaining genes in the second parent's order
    for i in range(parent2.genome_length()):
        # If the current gene is not yet in the child
        if not parent2.get_gene(i) in child.genes:
            # Loop to find a free position in the child's genome
            for j in range(child.genome_length()):
                if child.get_gene(j) is None:
                    child.set_gene(j, parent2.get_gene(i))
                    child_str[j] = Printer.blue("_")
                    break
    if Config.print_crossover:
        print("Crossover finished: %s." % "".join(child_str))

    return child


def crossover_random(parent1, parent2):
    """
    Random crossover algorithm
    We randomly select one parent as origin for each gene of the child

    :param parent1: The first parent
    :param parent2: The second Parent
    :return: The newly created child
    :type parent1 Individual
    :type parent2 Individual
    """
    child = Menu()
    genome_length = min(parent1.genome_length(), parent2.genome_length())
    child_str = [""] * genome_length
    child.genes = [None] * genome_length
    for i in range(genome_length):
        # If we are still before the end position, copy gene
        if random.random() < 0.5:
            child.set_gene(i, parent1.get_gene(i))
            child_str[i] = Printer.green("-")
        else:
            child.set_gene(i, parent2.get_gene(i))
            child_str[i] = Printer.blue("_")

    if Config.print_crossover:
        print("Crossover of length %d finished: %s." % (genome_length, "".join(child_str)))

    return child


def mutate_random(individual):
    """
    Random mutation algorithm

    :param individual: The trip that will be mutated
    :return: The trip after his mutation
    :type individual Individual
    :rtype Individual
    """
    gene_str = ""
    mut_str = ""
    digit_format = "%" + str(math.ceil(math.log10(Config.parameters[Config.KEY_NB_DISHES]))) + "d."
    genome_length = individual.genome_length()
    manager = MenuManager.get()
    for i in range(genome_length):
        assert (i < genome_length)

        index = manager.get_index(individual.get_gene(i))
        index_str = digit_format % index
        gene_str += index_str
        if random.random() < Config.parameters[Config.KEY_MUTATION_RATE]:
            gene = manager.get_random()
            individual.set_gene(i, gene)
            mut_str += digit_format % manager.get_index(gene)
        else:
            mut_str += index_str

    if Config.print_mutation:
        print("Individual of length %d mutated: %s" % (genome_length, Printer.print_diff(gene_str, mut_str, '. ')))


# @timer("Mutation") # uncomment to measure
def mutate(offset, population):
    """

    :param offset: Index at which we should start mutating individuals
    :param population: Population to mutate
    :return:
    """
    for i in range(offset, population.get_size()):
        algorithm_func['mutation'](population.get_at(i))


crossover_fails = 0
crossover_successes = 0


def evolve(population):
    """
    Evolves a population to its next state
    param population: The original population
    :return: The next iteration state of the received population
    :type population Population
    :rtype Population
    """
    next_state = Population(population.get_size(), False)

    # Elitism handling
    offset = 0
    if Config.parameters[Config.KEY_ELITISM]:
        next_state.save_at(0, population.get_fittest())
        offset = 1
    population_size = next_state.get_size()

    # Selection and crossover
    for i in range(offset, population_size):
        parent1 = algorithm_func['selection'](population)
        parent2 = algorithm_func['selection'](population)
        if parent1 == parent2:
            # print("Same parent(s): %s" % str(parent1))
            # crossover_fails += 1
            # tentatives = crossover_successes + crossover_fails
            # if tentatives > 100 and crossover_fails > 10 * crossover_successes:
            #     error_message = Printer.err(
            #         "Crossover: %d successes over %d tentatives." % (crossover_successes, tentatives))
            #     print(error_message, flush=True)
            #     raise ValueError("Failed crossover now amount to 10 times successful ones.")
            # TODO: Control useless crossovers
            child = parent1
        else:
            # crossover_successes += 1
            child = algorithm_func['crossover'](parent1, parent2)
        next_state.save_at(i, child)

    # Mutation
    mutate(offset, population)

    return next_state


def setup():  # FIXMEu
    algorithm_func['selection'] = tournament_selection
    algorithm_func['crossover'] = crossover_random
    algorithm_func['mutation'] = mutate_random

algorithm_func = {
    'selection': tournament_selection,
    'crossover': crossover_random,
    'mutation': mutate_random
}
