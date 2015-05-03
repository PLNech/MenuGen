from algorithms.model.factories import choose_method

__author__ = 'PLNech'

import subprocess
import sys
import os

from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt

from algorithms.model.menu.dish import Dish
from algorithms.model.menu.menu import Menu
from utils.config import Config


class Drawer:
    MIN_FIGURE_SIZE = 5
    MAX_FIGURE_SIZE = 100
    SCALING_FACTOR = 5
    OUTPUT_DIR_NAME = "img"

    @staticmethod
    def draw_trip(trip, name=None, detail=None, display=None, should_save_figure=True):
        """
        Draws a trip using matplotlib and networkx

        :param trip: the trip to draw
        :param name: name of the trip
        :param detail: a detail to add at the end of the title
        :param display: should we display the figure?
        :param should_save_figure: should we save the figure?

        :type trip: Trip
        :type name: str
        :type detail: str
        :type display: bool
        :type should_save_figure: bool

        :return: the filename of the created file
        :rtype: str
        """
        cities = trip.genes
        length = trip.get_score()
        if name is None:
            filename = "%dcities_%dkm" % (len(cities), int(length))
            name = "Trip of %d km across %d towns." % (length, len(cities))
        else:
            filename = name.replace(" ", "_").lower() + "_%dcities_%dkm" % (len(cities), int(length))
            name = name.capitalize() + ": %d km across %d towns." % (length, len(cities))

        return Drawer.draw_cities(cities, name, filename, detail, display, should_save_figure)

    @staticmethod
    def save_figure(filename, name, figure=None, legend=None):
        print("Saving %s..." % name)
        filename = os.path.join(Drawer.OUTPUT_DIR_NAME, filename + ".png")
        if not os.path.exists(Config.folder_name_output):
            os.makedirs(Config.folder_name_output)
        with open(filename, "w") as f:
            handler = figure if figure is not None else plt
            print("handler:", handler)
            handler.savefig(f, bbox_extra_artists=(legend,), bbox_inches='tight')
            plt.close()
            plt.clf()
            print("Saved figure as %s." % filename)
        return filename

    @staticmethod
    def display_both(filename1, filename2):
        """
        Displays two pictures
        """
        Drawer.display_pic(filename1)
        Drawer.display_pic(filename2)

    @staticmethod
    def display_pic(filename):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filename))
        elif os.name == 'nt':
            os.startfile(filename)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filename))

    @staticmethod
    def draw_steps(run, should_display=False, should_save_figure=True):
        menu_sizes = []
        calories = []
        proteins = []
        carbohydrates = []
        fats = []
        name = run.name
        for i, menu in enumerate(run.steps):
            menu_sizes.append(menu.genome_length())
            calories.append(menu.get_calories())
            proteins.append(menu.get_proteins())
            carbohydrates.append(menu.get_carbohydrates())
            fats.append(menu.get_fats())

        filename = "run_" + name.replace(" ", "_").lower() + "_%d_dishes,_%d_generations" % (
            Config.parameters[Config.KEY_NB_DISHES], Config.parameters[Config.KEY_NB_GENERATION])
        fig = plt.figure()
        plt.text(0.5, 0.6, name,
                 horizontalalignment='center',
                 transform=plt.gca().transAxes,
                 fontsize=20)

        # X-axis
        plt.xlabel("Number of steps")
        plt.axes().get_xaxis().set_major_locator(MaxNLocator(integer=True))  # Force integer type
        plt.xlim((0, len(run.steps)))

        # # Left y-axis
        # ax0 = fig.add_subplot(111)
        # line0, = ax0.plot(menu_sizes, 'k-')
        # plt.ylabel("Amount of dishes per menu")
        plt.ylim((0.0, 1.0))

        # Right y-axis
        ax1 = fig.add_subplot(111,
                              # sharex=ax0,
                              frameon=False)
        ax1.xaxis.set_visible(False)
        line1, = ax1.plot(calories, 'xk-')

        ax1.yaxis.tick_right()
        ax1.yaxis.set_label_position("right")
        plt.ylabel("Nutritive quality")

        ax2 = fig.add_subplot(111,
                              sharex=ax1,
                              frameon=False)
        ax2.xaxis.set_visible(False)
        ax2.yaxis.set_visible(False)
        line2, = ax2.plot(proteins, 'xr-')

        ax3 = fig.add_subplot(111, sharex=ax2, frameon=False)
        ax3.xaxis.set_visible(False)
        ax3.yaxis.set_visible(False)
        line3, = ax3.plot(carbohydrates, 'xc-')

        ax4 = fig.add_subplot(111, sharex=ax3, frameon=False)
        ax4.xaxis.set_visible(False)
        ax4.yaxis.set_visible(False)
        line4, = ax4.plot(fats, 'xy-')

        legend = plt.legend((
            # line0,
            line1, line2, line3, line4), (
            "Calories", "Proteins", "Carbohydrates", "Fats"),
            bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
            mode="expand")

        if should_display:
            plt.show()
        if should_save_figure:
            filename = Drawer.save_figure(filename, name, fig, legend)
        return filename

    @staticmethod
    def draw_menu(menu, name=None, detail=None, should_display=False, should_save_figure=True):
        """

        :type menu: Menu
        :type name: str
        :type detail: str
        :type should_display: bool
        :type should_save_figure: bool
        """
        weights = [dish.calories for dish in menu.genes]
        tastes = [dish.quality for dish in menu.genes]

        filename = name.replace(" ", "_").lower() + "_%ddishes_%.1f%%" % (len(menu.genes), menu.get_fitness() * 100)
        fig = plt.figure()
        plt.text(0.5, 0.9, name,
                 horizontalalignment='center',
                 transform=plt.gca().transAxes,
                 fontsize=20)
        if detail is not None:
            plt.text(0.5, 0.8, detail,
                     horizontalalignment='center',
                     transform=plt.gca().transAxes,
                     fontsize=15)

        # X-axis
        plt.xlabel("Index of dish")
        plt.axes().get_xaxis().set_major_locator(MaxNLocator(integer=True))  # Force integer type

        # Left y-axis
        ax1 = fig.add_subplot(111)
        line1, = ax1.plot(weights, 'o')
        plt.ylabel("Amount of calories per meal")

        # Right y-axis
        ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
        line2, = ax2.plot(tastes, 'or')
        ax2.yaxis.tick_right()
        ax2.yaxis.set_label_position("right")
        plt.ylabel("Tastiness of dish")

        # TODO: Solve axes range mayhem
        # plt.axis((0, len(menu.genes), 0, Config.parameters[Config.KEY_BAG_SIZE]))
        # plt.axis((0, len(menu.genes), 0.0, 1.0))

        legend = plt.legend((line1, line2), ("Quality", "Quantity"), bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                            mode="expand")
        if should_display:
            plt.show()
        if should_save_figure:
            filename = Drawer.save_figure(filename, name, fig, legend)
        return filename
