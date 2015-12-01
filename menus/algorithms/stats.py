import logging
from collections import defaultdict
from copy import deepcopy
from math import sqrt

from menus.algorithms.model.factories import choose_method
from menus.algorithms.model.menu.menu import Menu
from menus.algorithms.utils.calc import Calc
from menus.algorithms.utils.config import Config
from menus.algorithms.utils.printer import Printer
from menus.algorithms.utils.singleton import singleton

__author__ = 'PLNech'

logger = logging.getLogger("menus")


class Statistics:
    """
    Statistics holder object
    Mean = Mean value in float
    Median = Median value in float
    Mode = Mode value in float
    Efficacy = Difference of fitnesses between first and last generations
    Efficiency = Average difference of fitness between each generation
    Variance = Average of the squares of centered values (differences of values and average)
    Standard deviation = Square root of the variance (as squares did increase values, measure of dispersion)
    Median absolute deviation = Median of the absolute deviations from the median (robust estimator of dispersion)
    """

    def __init__(self, mean, median, mode, efficacy, efficiency, variance, mad):
        self.mean = mean
        self.median = median
        self.mode = mode
        self.efficacy = efficacy
        self.efficiency = efficiency
        self.variance = variance
        self.stddev = sqrt(variance)
        self.mad = mad

    def __str__(self):
        return "mean: %.2f, " % self.mean + \
               "median: %.2f, " % self.median + \
               "mode: %.2f, " % self.mode + \
               "efficacy: %.3f%%, " % self.efficacy + \
               "efficiency: %.3f." % self.efficiency + \
               "variance: %.2f, " % self.variance + \
               "deviation: %.2f, " % self.stddev + \
               "mean average deviation: %.2f." % self.mad


class MenuStep(Menu):
    def __init__(self, generation, dishes):
        super().__init__(dishes)
        self.generation = generation


class Run():
    def __init__(self, name, nb_turns):
        self.name = name
        self.steps = []
        self.nb_turns = nb_turns

    def __str__(self):
        ret_str = "Run %s:\n" % self.name
        for step in self.steps:
            score_str = step.print_score()
            score = step.get_score()
            step_repr = Printer.print_menu(step)
            ret_str += "Step %s: %s (%f)- %s\n" % ("{:02}".format(step.generation), score_str, score, step_repr)
        return ret_str

    def add_step(self, step):
        self.steps.append(deepcopy(step))

    def add(self, generation, genes):  # TODO Cleanup
        step = choose_method(MenuStep,
                             MenuStep,
                             (generation, genes))
        self.add_step(step)


class StatKeeper(singleton):
    runs = {}

    @staticmethod
    def new_run(run_name, nb_turns):
        if run_name in StatKeeper.runs:
            logger.info(Printer.err("Error: a run named %s already exists: %s" %
                                    (run_name, str(StatKeeper.get_run(run_name)))))
            exit(1)
        StatKeeper.runs[run_name] = Run(run_name, nb_turns)

    @staticmethod
    def save_progress(run_name, generation, genes):
        if run_name not in StatKeeper.runs:
            logger.err("Error: no run named %s." % run_name)
            exit(1)
        StatKeeper.get_run(run_name).add(generation, genes)

    @staticmethod
    def get_run(run_name):
        """
        :type run_name: str
        :rtype: Run
        """
        if run_name not in StatKeeper.runs:
            logger.err("Error: no run named %s." % run_name)
            exit(1)
        return StatKeeper.runs[run_name]

    @staticmethod
    def clear():
        StatKeeper.runs.clear()

    @staticmethod
    def get_progress(run_name):
        run = StatKeeper.get_run(run_name)
        return str(run)

    @staticmethod
    def generate_stats():
        """
        Calculates the average efficacy and efficiency of all runs
        both values are calculated together for performance

        :return: a Statistics object with the computed values
        :rtype Statistics
        """
        values = []
        sum_distances = 0
        sum_efficiencies = 0
        sum_efficacies = 0
        nb_runs = len(StatKeeper.runs)

        # Calculate average distance, efficacy and efficiency
        for key in StatKeeper.runs:
            run = StatKeeper.runs[key]
            init_score = run.steps[0].get_score()
            final_score = run.steps[-1].get_score()
            efficacy, efficiency = StatKeeper.calculate_effs(init_score, final_score)
            sum_efficacies += efficacy
            sum_efficiencies += efficiency
            sum_distances += final_score
            values.append(final_score)
        avg_distance = sum_distances / nb_runs
        avg_efficacy = sum_efficacies / nb_runs
        avg_efficiency = sum_efficiencies / nb_runs

        var = Calc.variance(values, avg_distance)

        # Calculate median
        med_distance = Calc.median(values)

        # Calculate mode
        frequencies = defaultdict(int)
        for v in values:
            str_v = "%.2f" % v
            frequencies[str_v] += 1
        mode_distance = max(values, key=lambda i: frequencies[i])

        mad = Calc.median_absolute_deviation(med_distance, values)
        return Statistics(avg_distance, med_distance, mode_distance, avg_efficacy, avg_efficiency, var, mad)

    @staticmethod
    def print_run_stats(efficacy_str, efficiency_str, init_fittest, final_fittest, run_name):
        final_result = final_fittest.print_score()
        logger.info("Run ended.")
        logger.info("Progress evolution of %s:\n%s" % (run_name, StatKeeper.get_progress(run_name)))
        logger.info("Final %s: %s." % (Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]],
                                       final_result))
        logger.info("Final menu:\n%s." % Printer.print_menu(final_fittest))
        logger.info("Efficacy: new menu is %s better than older one. (%s -> %s)"
                    % (efficacy_str, init_fittest.get_score(), final_fittest.get_score()))
        logger.info("Efficiency: we gained an average improvement of %s per iteration.\n"
                    % efficiency_str)

    @staticmethod
    def print_statistics(init_score):
        statistics = StatKeeper.generate_stats()
        average = statistics.mean
        avg_efficacy = statistics.efficacy
        avg_efficiency = statistics.efficiency
        standard_deviation = statistics.stddev
        median_average_deviation = statistics.mad
        mean_length = init_score - average
        median_length = init_score - statistics.median
        mode_length = init_score - statistics.mode
        avg_efficacy_str = "%+2.f%%" % (avg_efficacy * 100)
        if Config.parameters[Config.KEY_SOLUTION_TYPE] == "Trip":  # Todo: Consider generic solution
            avg_efficiency_str = "%d units" % avg_efficiency
        else:
            avg_efficiency_str = "%.3f" % avg_efficiency

        normalised_deviation_str = "%+.2f%%" % (100 * standard_deviation / average)
        normalised_mad_str = "%+.2f%%" % (100 * median_average_deviation / average)
        normalised_efficiency_str = "%+.3f%%" % (avg_efficiency / mean_length)
        normalised_mean_str = "%+.2f%%" % (100 * mean_length / init_score)
        normalised_median_str = "%+.2f%%" % (100 * median_length / init_score)
        normalised_mode_str = "%+.2f%%" % (100 * mode_length / init_score)
        score_unit = Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]]

        logger.info("Efficacy: solutions were on average %s better than first one. (%d -> %d: %d)"
                    % (Printer.green(avg_efficacy_str), init_score, average, mean_length))
        logger.info("Efficiency: average progress of %s per iteration (%s)."
                    % (Printer.green(avg_efficiency_str), normalised_efficiency_str))
        logger.info("Total %s: average %.2f, median %.2f, mode %.2f."
                    % (score_unit, average, statistics.median, statistics.mode))
        logger.info("Gained %s: average %s, median %s, mode %s."
                    % (score_unit, normalised_mean_str, normalised_median_str, normalised_mode_str))
        logger.info("Standard deviation of solutions %ss: %s."
                    % (score_unit, normalised_deviation_str))
        logger.info("Median absolute deviation of solutions %ss: %s."
                    % (score_unit, normalised_mad_str))

    @staticmethod
    def calculate_effs(init_score, final_score):
        return choose_method(StatKeeper.calculate_effs_trip,
                             StatKeeper.calculate_effs_menu,
                             (init_score, final_score))

    @staticmethod
    def calculate_effs_menu(init_score, final_score):
        efficacy = final_score - init_score
        efficiency = efficacy / Config.parameters[Config.KEY_NB_GENERATION]
        return efficacy, efficiency

    @staticmethod
    def calculate_effs_trip(init_score, final_score):
        efficacy = 1 - final_score / init_score
        efficiency = (init_score - final_score) / Config.parameters[Config.KEY_NB_GENERATION]
        return efficacy, efficiency
