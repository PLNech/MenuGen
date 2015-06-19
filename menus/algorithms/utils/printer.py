__author__ = 'PLNech'

from menus.algorithms.utils.config import Config


class Printer():
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = "\033[1m"

    @staticmethod
    def disable():
        Printer.HEADER = ''
        Printer.BLUE = ''
        Printer.GREEN = ''
        Printer.WARNING = ''
        Printer.FAIL = ''
        Printer.END = ''

    @staticmethod
    def green(msg):
        return Printer.color(msg, Printer.GREEN)

    @staticmethod
    def blue(msg):
        return Printer.color(msg, Printer.BLUE)

    @staticmethod
    def red(msg):
        return Printer.color(msg, Printer.RED)

    @staticmethod
    def bold(msg):
        return Printer.color(msg, Printer.BOLD)

    @staticmethod
    def color(msg, color):
        return str(color) + str(msg) + str(Printer.END)

    @staticmethod
    def info(msg):
        return Printer.blue(msg)

    @staticmethod
    def warn(msg):
        print(Printer.WARNING + msg + Printer.END)

    @staticmethod
    def err(msg):
        return Printer.red(msg)

    @staticmethod
    def if_bigger(msg, v1, v2):
        if v1 == v2:
            return Printer.bold(msg)
        elif v1 < v2 or float(v1) < float(v2) or int(v1 < int(v2)):
            return Printer.red(msg)
        else:
            return Printer.green(msg)

    @staticmethod
    def if_positive(msg, value):
        if value == 0:
            return Printer.bold(msg)
        elif value < 0:
            return Printer.red(msg)
        else:
            return Printer.green(msg)

    @staticmethod
    def print_menu(menu):  # TODO: Print unique meal ids instead of menu-wise statistics
        """
        Prints the score of a menu
        :type menu: Menu
        :return: A string representation of the menu's score
        """
        menu_size = menu.genome_length()
        calories = menu.calories
        proteins = menu.proteins
        carbohydrates = menu.carbohydrates
        fats = menu.fats
        fit_calories = menu.get_calories()
        fit_proteins = menu.get_proteins()
        fit_carbohydrates = menu.get_carbohydrates()
        fit_fats = menu.get_fats()
        fitness_percent = menu.get_fitness() * 100
        return "%d meals: Calories %i->%.2f|Proteins %i->%.2f|Carbohydrates %i->%.2f|Fats %i->%.2f -> %.1f%%|%s" % (
            menu_size, calories, fit_calories, proteins, fit_proteins,
            carbohydrates, fit_carbohydrates, fats, fit_fats, fitness_percent, str(menu))

    @staticmethod
    def print_diff(str1, str2, ignore_chars="-> "):
        len1, len2 = len(str1), len(str2)
        try:
            assert (len1 == len2)
        except AssertionError:
            print("The given strings are of different lengths: _%s_/_%s_ (%d/%d)." % (str1, str2, len1, len2))
            raise

        list_str = ""
        for c1, c2 in zip(str1, str2):
            if c1 in ignore_chars:
                list_str = list_str + c1
            elif c1 == c2:
                list_str += Printer.green(c1)
            else:
                list_str += Printer.red(c2)
        return list_str

    @staticmethod
    def print_and_log(message, f):
        """

        :param message: The message to process
        :type message str
        :param f: The file descriptor of the file
        :type f file
        """
        print(message)
        f.write(message + "\n")

    @staticmethod
    def print_gen_score(best_individual, generation, run_name):
        best_score = best_individual.get_score()
        best_str = Printer.print_menu(best_individual)
        dimension = Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]]
        print("Run %s, Generation %i - best %s found yet: %.2f - %s" % (run_name, generation, dimension, best_score,
                                                                        best_str),
              end="\r")

    @staticmethod
    def print_final(initial_value, best_value, run_name):
        solution_type = Config.parameters[Config.KEY_SOLUTION_TYPE]
        improvement = best_value - initial_value
        print("Run %s - best %s found: %.2f%s. (%+.2f%%)" % (
            run_name, Config.score_dimensions[solution_type],
            best_value, Config.score_units[solution_type],
            improvement))

    @staticmethod
    def print_init():
        print("Bonjour, gourmet!")
        print("Evolving %d generations of %d individuals eating up to %d dishes in a set of %d." %
              (Config.parameters[Config.KEY_NB_GENERATION],
               Config.parameters[Config.KEY_POPULATION_SIZE],
               Config.parameters[Config.KEY_MAX_DISHES],
               Config.parameters[Config.KEY_NB_DISHES]))

    @staticmethod
    def print_run_init(init_length, init_fittest):
        print("Initial %s: %i." % ((Config.score_dimensions[Config.parameters[Config.KEY_SOLUTION_TYPE]]), init_length))
        print("Initial menu:\n%s" % Printer.print_menu(init_fittest))
