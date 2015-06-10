import menus.algorithms.algorithm as algorithm
from menus.algorithms.model.menu.menu_manager import MenuManager

__author__ = 'PLNech'

# from numpy import arange
import argparse
import os
import sys

from menus.algorithms.utils.config import Config
from menus.algorithms.stats import StatKeeper
# from utils.drawer import Drawer
from menus.algorithms.utils.printer import Printer
from menus.algorithms.model.population import Population
from menus.algorithms.model.factories import Factory, is_better_than

stats = StatKeeper


def run(run_name, init_fittest=None):
    # New run
    manager = MenuManager.get()
    nb_dishes = len(manager.dishes)
    stats.new_run(run_name, Config.parameters[Config.KEY_NB_GENERATION])
    population = Population(Config.parameters[Config.KEY_POPULATION_SIZE])

    if init_fittest is None:
        init_fittest = population.get_at(0)
    init_score = init_fittest.get_score()
    stats.save_progress(run_name, 0, init_fittest.genes)

    if Config.draw_all:
        run_name_all = run_name + "_all"
        stats.new_run(run_name_all, Config.parameters[Config.KEY_NB_GENERATION])
        stats.save_progress(run_name_all, 0, init_fittest.genes)

    if Config.print_each_run:
        Printer.print_run_init(init_score, init_fittest)

    population = algorithm.evolve(population)
    if is_better_than(sys.maxsize, 0):
        old_best = 0
    else:
        old_best = sys.maxsize

    for generation_i in range(Config.parameters[Config.KEY_NB_GENERATION]):
        stat_index = generation_i + 1  # the first individual was already added in stats
        population = algorithm.evolve(population)
        best_individual = population.get_fittest()
        best_score = best_individual.get_score()

        if is_better_than(best_score, old_best):
            stats.save_progress(run_name, stat_index, best_individual.genes)
            old_best = best_score
        if Config.draw_all:
            stats.save_progress(run_name_all, stat_index, best_individual.genes)

        if Config.print_generation:
            if generation_i < Config.parameters[Config.KEY_NB_GENERATION] - 1:
                Printer.print_gen_score(best_individual, generation_i, run_name)
            else:
                Printer.print_final(init_score, best_score, run_name)

    final_fittest = population.get_fittest()
    final_score = final_fittest.get_score()
    solution_type = Config.parameters[Config.KEY_SOLUTION_TYPE]

    efficacy, efficiency = stats.calculate_effs(init_score, final_score)
    efficacy_str_raw = "%+.1f%%" % (efficacy * 100)
    efficacy_str_color = Printer.if_positive(efficacy_str_raw, efficacy)
    efficiency_format = "%2d" if solution_type is "Trip" else "%+.3f"  # TODO: Cleanup
    efficiency_str_raw = efficiency_format % (efficiency * 100)
    efficiency_str_color = Printer.if_positive(efficiency_str_raw, efficiency)

    if Config.print_each_run:
        stats.print_run_stats(efficacy_str_color, efficiency_str_color, init_fittest, final_fittest, run_name)

    print("Final fittest:")
    print(final_fittest)
    return final_fittest


def init_log(log_filename):
    if not os.path.exists(Config.folder_name_log):
        os.makedirs(Config.folder_name_log)
    f = open(os.path.join(Config.folder_name_log, log_filename), 'w')
    return f


# def run_test(parameter="population_size", begin=1, end=100):
# """
#     Test several values of a parameter to find optimal one
#     :param parameter: The key in Config.parameters of a parameter to test
#     :type parameter str
#     :param begin: first value of test range
#     :type begin float
#     :param end: last value of test range
#     :type end float
#     """
#     # TODO: Take time into account
#
#     Config.print_each_run = False
#     Config.parameters[Config.KEY_RUN_NUMBER] = 20
#
#     best_score = sys.maxsize
#     best_mean = sys.maxsize
#     best_median = sys.maxsize
#     best_mode = sys.maxsize
#     best_efficacy = 0
#     best_efficiency = 0
#
#     best_dist_param = -42
#     best_mean_param = -42
#     best_median_param = -42
#     best_mode_param = -42
#     best_efficacy_param = -42
#     best_efficiency_param = -42
#
#     interval = (begin, end)  # inclusive
#     step = (end - begin) / Config.parameters[Config.KEY_NB_TEST_STEPS]
#     values = arange(begin, end, step)
#     statistics = {}
#
#     log_filename = parameter + "(%.3f,%.3f).log" % (begin, end)
#     f = init_log(log_filename)
#     f.write("Initial %s: %i.\n" % (Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]],
#                                    init_score))
#
#     for v in values:
#         if parameter not in Config.parameters:
#             raise KeyError("%s is not a defined parameter." % parameter)
#         Config.parameters[parameter] = v
#
#         for run_i in range(Config.parameters[Config.KEY_RUN_NUMBER]):
#             run_name = str(run_i) + "-" + str(v) + "/" + str(interval[1])
#             final_fittest = run(run_name)
#             final_score = final_fittest.get_score()
#
#             statistics = StatKeeper.generate_stats()
#
#             if is_better_than(final_score, best_score):
#                 best_score = final_score
#                 best_dist_param = v
#
#             if is_better_than(statistics.mean, best_mean):
#                 best_mean = statistics.mean
#                 best_mean_param = v
#
#             if is_better_than(statistics.median, best_median):
#                 best_median = statistics.median
#                 best_median_param = v
#
#             if is_better_than(statistics.mode, best_mode):
#                 best_mode = statistics.mode
#                 best_mode_param = v
#
#             if statistics.efficacy > best_efficacy:
#                 best_efficacy = statistics.efficacy
#                 best_efficacy_param = v
#
#             if statistics.efficiency > best_efficiency:
#                 best_efficiency = statistics.efficiency
#                 best_efficiency_param = v
#
#         message = "End of simulation : %s=%.3f - %s" % (parameter, v, str(statistics))
#         Printer.print_and_log(message, f)
#         f.flush()
#
#     print("End of test.")
#     Printer.print_and_log("best_score value = %.3f (%.2f)" % (best_dist_param, best_score), f)
#     Printer.print_and_log("best_mean value = %.3f (%.2f)" % (best_mean_param, best_mean), f)
#     Printer.print_and_log("best_median value = %.3f (%.2f)" % (best_median_param, best_median), f)
#     Printer.print_and_log("best_mode value = %.3f (%.2f)" % (best_mode_param, best_mode), f)
#     Printer.print_and_log("best_efficacy value = %.3f (%.2f%%)" % (best_efficacy_param, best_efficacy), f)
#     Printer.print_and_log("best_efficiency value = %.3f (%.2f)" % (best_efficiency_param, best_efficiency), f)
#
#     f.flush()
#     f.close()


def run_standard(init_fittest=None, run_name="run"):
    nb_runs = Config.parameters[Config.KEY_RUN_NUMBER]
    nb_gens = Config.parameters[Config.KEY_NB_GENERATION]
    nb_pop = Config.parameters[Config.KEY_POPULATION_SIZE]

    for run_i in range(0, nb_runs):
        if nb_runs > 1:
            run_name = str(run_i)
        final_fittest = run(run_name, init_fittest)

    print("Simulation ended.")

    if nb_runs > 1 and init_fittest is not None:
        StatKeeper.print_statistics(init_fittest.get_score())
    return final_fittest


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', type=int, help='size of the population')
    parser.add_argument('-r', '--runs', type=int, help='number of runs to execute')
    parser.add_argument('-t', '--type', type=str, help='type of solution to search')

    args = vars(parser.parse_args())

    if args['size'] is not None:
        Config.parameters[Config.KEY_POPULATION_SIZE] = args['size']
    if args['runs'] is not None:
        Config.parameters[Config.KEY_RUN_NUMBER] = args['runs']
    if args['type'] is not None:
        Config.parameters[Config.KEY_SOLUTION_TYPE] = args['type']

    Printer.print_init()

    # First individual for comparison
    # we use the same one to bench all runs
    main_pop = Population(1)
    main_first = main_pop.get_at(0)
    if not Config.print_each_run:
        print("Initial %s: %i." % (Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]],
                                   main_first.get_score()))

    algorithm.setup()
    # run_test("mutation_rate", 0.25, 0.5)
    run_standard(main_first)
