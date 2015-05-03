__author__ = 'PLNech'

import random
import math
import multiprocessing

from algorithms.model.factories import Factory, choose_method
from utils.config import Config
from utils.printer import Printer
from utils.multi import cpu_count
from algorithms.model.population import Population
from algorithms.model.individual import Individual


def mutate(individual):
    """
    Wrapper to call the chosen mutation algorithm

    :param individual: The individual that will be mutated
    :return: The individual after his mutation
    :type individual individual
    :rtype individual
    """
    return Algorithm.mutate_swap(individual)


class Algorithm:
    @staticmethod
    def func_selection(population):
        """
        :type population Population
        :rtype Individual
        """
        individual = population.get_at(0)
        return individual

    @staticmethod
    def func_crossover(parent1, parent2):
        """
        :type parent1 Individual
        :type parent2 Individual
        :rtype Individual
        """
        return parent2 if parent2 is None else parent1

    @staticmethod
    def func_mutation(individual):
        """
        :type individual Individual
        :rtype Individual
        """
        return individual

    @staticmethod
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

    @staticmethod
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
        child = Factory.individual()

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

    @staticmethod
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
        child = Factory.individual()
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

    @staticmethod
    def mutate_swap(trip):
        """
        Swap mutation algorithm
        We randomly select two objects and swap their positions.
        By only swapping objects, we avoid introducing any duplicate
        in our solution.

        :param trip: The trip that will be mutated
        :return: The trip after his mutation
        :type trip Trip
        :rtype Trip
        """
        before_path = ""
        if Config.print_mutation:
            before_path = Printer.print_path(trip)

        genome_length = trip.genome_length()
        mutation_repr = [i for i in range(genome_length)]
        for pos1 in range(genome_length):
            if random.random() < Config.parameters[Config.KEY_MUTATION_RATE]:
                pos2 = random.randint(0, genome_length - 1)

                # Swap two cities at random positions
                trip.swap(pos1, pos2)
                mutation_repr[pos1], mutation_repr[pos2] = mutation_repr[pos2], mutation_repr[pos1]

        if Config.print_mutation:
            after_path = Printer.print_path(trip)
            if before_path != after_path:
                print(Printer.print_diff(before_path, after_path))

        return trip

    @staticmethod
    def mutate_invert(trip):
        """
        Crossover inversion algorithm
        For each gene to be mutated, set a random length and invert the following sequence of genes of that length
        :param trip: The trip that will be mutated
        :return: The trip after his mutation
        :type trip Trip
        :rtype Trip
        """
        before_path = ""
        if Config.print_mutation:
            before_path = Printer.print_path(trip)

        genome_length = trip.genome_length()
        mutation_repr = [i for i in range(genome_length)]
        for pos1 in range(genome_length):
            if random.random() < Config.parameters[Config.KEY_MUTATION_RATE]:
                pos2 = random.randint(0, genome_length - 1)

                # Swap the cities between the two positions
                trip.invert_sequence(pos1, pos2)
                mutation_repr[pos1], mutation_repr[pos2] = mutation_repr[pos2], mutation_repr[pos1]

        if Config.print_mutation:
            after_path = Printer.print_path(trip)
            if before_path != after_path:
                print(Printer.print_diff(before_path, after_path))

        return trip

    @staticmethod
    def mutate_random(individual):
        """
        Random mutation algorithm

        :param individual: The trip that will be mutated
        :return: The trip after his mutation
        :type individual Individual
        :rtype Individual
        """
        manager = Factory.manager()
        gene_str = ""
        mut_str = ""
        digit_format = "%" + str(math.ceil(math.log10(Config.parameters[Config.KEY_NB_DISHES]))) + "d."
        genome_length = individual.genome_length()
        for i in range(genome_length):
            assert (i < genome_length)
            index = manager.get_index(individual.get_gene(i))
            index_str = digit_format % index
            gene_str += index_str
            if random.random() < Config.parameters[Config.KEY_MUTATION_RATE]:
                gene = Factory.gene()
                individual.set_gene(i, gene)
                mut_str += digit_format % manager.get_index(gene)
            else:
                mut_str += index_str

        if Config.print_mutation:
            print("Individual of length %d mutated: %s" % (genome_length, Printer.print_diff(gene_str, mut_str, '. ')))


    @staticmethod
    # @timer("Sequential") # uncomment to measure
    def mutate_sequential(offset, population):
        """

        :param offset: Index at which we should start mutating individuals
        :param population: Population to mutate
        :return:
        """
        for i in range(offset, population.get_size()):
            Algorithm.func_mutation(population.get_at(i))

    @staticmethod
    # @timer("Parallel") # uncomment to measure
    def mutate_parallel(offset, population):  # TODO: Handle offset, even if this is meaningless
        """
        Test of parallelisation
        This is currently way slower than sequential!

        :param population: The population to mutate
        """
        with multiprocessing.Pool(cpu_count()) as p:
            p.map(mutate, population.population)

    crossover_fails = 0
    crossover_successes = 0

    @staticmethod
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
            parent1 = Algorithm.func_selection(population)
            parent2 = Algorithm.func_selection(population)
            if parent1 == parent2:
                Algorithm.crossover_fails += 1
                tentatives = Algorithm.crossover_successes + Algorithm.crossover_fails
                if tentatives > 100 and Algorithm.crossover_fails > 10 * Algorithm.crossover_successes:
                    error_message = Printer.err(
                        "Crossover: %d successes over %d tentatives." % (Algorithm.crossover_successes, tentatives))
                    print(error_message, flush=True)
                    # raise ValueError("Failed crossover now amount to 10 times successful ones.")
                # TODO: Control useless crossovers
                child = parent1
            else:
                Algorithm.crossover_successes += 1
                child = Algorithm.func_crossover(parent1, parent2)
            next_state.save_at(i, child)

        # Mutation
        Algorithm.mutate_sequential(offset, population)

        return next_state

    @staticmethod
    def setup():
        choose_method(Algorithm.setup_trip,
                      Algorithm.setup_menu,
                      None)

    @staticmethod
    def setup_trip():
        Algorithm.func_selection = Algorithm.tournament_selection
        Algorithm.func_crossover = Algorithm.crossover_ordered
        Algorithm.func_mutation = Algorithm.mutate_invert

    @staticmethod
    def setup_menu():
        Algorithm.func_selection = Algorithm.tournament_selection
        Algorithm.func_crossover = Algorithm.crossover_random
        Algorithm.func_mutation = Algorithm.mutate_random
