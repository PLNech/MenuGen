import os

__author__ = 'PLNech'

from menus.algorithms.dietetics import DieteticsNeeds
from menus.algorithms.model.menu.menu_manager import MenuManager

from menus.algorithms.model.individual import Individual
from menus.algorithms.model.menu.dish import Dish
from menus.algorithms.utils.config import Config


class Menu(Individual):  # TODO Document!
    # noinspection PyMissingConstructor
    # The parent constructor raises an exception as being abstract
    def __init__(self, genes=None):
        if genes is not None:
            self.genes = genes
        else:
            self.genes = []
        self.fitness = 0
        self.fitness_calories = 0
        self.fitness_proteins = 0
        self.fitness_carbohydrates = 0
        self.fitness_fats = 0
        self.calories = 0
        self.proteins = 0
        self.carbohydrates = 0
        self.fats = 0


    def __str__(self):
        ret_str = "["
        for dish in self.genes:
            ret_str += str(dish)
        return ret_str + "]"

    def __repr__(self):
        return "Menu" + str(self)

    def get_calories(self):
        if self.fitness_calories == 0:
            self.get_score()
        return self.fitness_calories

    def get_proteins(self):
        if self.fitness_proteins == 0:
            self.get_score()
        return self.fitness_proteins

    def get_carbohydrates(self):
        if self.fitness_carbohydrates == 0:
            self.get_score()
        return self.fitness_carbohydrates

    def get_fats(self):
        if self.fitness_fats == 0:
            self.get_score()
        return self.fitness_fats

    def get_fitness(self):
        if self.fitness == 0:
            self.get_score()
        return self.fitness

    def get_score(self, objectives=None):
        """

        :param objectives: Objectives to reach
        :type objectives DieteticsNeeds
        :return:
        """
        if self.fitness != 0:
            return self.fitness
        if objectives is None:
            objective_calories = Config.parameters[Config.KEY_MAX_DISH_CALORIES]
            objective_proteins = Config.parameters[Config.KEY_MAX_DISH_PROTEINS]
            objective_carbohydrates = Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES]
            objective_fats = Config.parameters[Config.KEY_OBJECTIVE_FATS]
        else:
            objective_calories = objectives.calories
            objective_proteins = objectives.grams_proteins
            objective_carbohydrates = objectives.grams_carbohydrates
            objective_fats = objectives.grams_fats

        accu_calories = 0
        accu_proteins = 0
        accu_carbs = 0
        accu_fats = 0
        for dish in self.genes:
            accu_calories += dish.calories
            accu_proteins += dish.proteins
            accu_carbs += dish.carbohydrates
            accu_fats += dish.fats

        self.calories = accu_calories
        self.proteins = accu_proteins
        self.carbohydrates = accu_carbs
        self.fats = accu_fats

        self.fitness_calories = self.nutrient_fitness(accu_calories, objective_calories)
        self.fitness_proteins = self.nutrient_fitness(accu_proteins, objective_proteins)
        self.fitness_carbohydrates = self.nutrient_fitness(accu_carbs, objective_carbohydrates)
        self.fitness_fats = self.nutrient_fitness(accu_fats, objective_fats)

        # Global fitness is 40% calories, 20% proteins, 20% carbohydrates and 20% fats
        self.fitness = (self.fitness_calories * 2 +
                        self.fitness_proteins + self.fitness_carbohydrates + self.fitness_fats) / 5
        return self.fitness

    def print_score(self):
        return "%.2f" % self.get_score()

    def genome_length(self):
        return len(self.genes)

    def get_gene(self, index):
        """
        Get the dish at given index of menu
        :type index: int
        :rtype: Dish
        """
        return self.genes[index]

    def set_gene(self, index, dish):
        """
        Set the gene at given index with given value
        :type index: int
        :type dish: Dish
        """
        self.genes[index] = dish
        self.fitness = 0
        self.fitness_calories = 0
        self.fitness_proteins = 0
        self.fitness_carbohydrates = 0
        self.fitness_fats = 0

    def generate(self):
        manager = MenuManager.get()

        accu_calories = 0
        over_size = 2439.7 * 7 * Config.parameters[Config.KEY_OVERWEIGHT_FACTOR]  # TODO: Use actual calories objective
        genes_length = Config.parameters[Config.KEY_MAX_DISHES]
        # random.randrange(0, Config.parameters[Config.KEY_MAX_DISHES])  # TODO: Consider random genome length
        for _ in range(genes_length):
            dish = manager.get_random()
            accu_calories += dish.calories
            if accu_calories + dish.calories > over_size:
                break
            else:
                accu_calories += dish.calories
                self.genes.append(dish)
                # print("Finished generating a menu of %d calories through %d dishes." %
                # (accu_calories, len(self.genes)))

    @staticmethod
    def nutrient_fitness(quantity, objective):  # TODO Note range of recommendations for finest fitness
        oversize = objective * Config.parameters[Config.KEY_OVERWEIGHT_FACTOR]
        if quantity <= objective:
            fitness = quantity / objective
        elif quantity <= oversize:
            over_amount = oversize - objective
            actual_amount = quantity - objective
            fitness = 1 - actual_amount / over_amount
        else:
            fitness = 0
        return fitness

    def print_short(self):
        str_array = []
        for i, gene in enumerate(self.genes):
            str_array.append(str(gene))
        return "M[" + "|".join(str_array) + "]"

    def print_fitness(self):
        calories = self.get_calories()
        proteins = self.get_proteins()
        carbohydrates = self.get_carbohydrates()
        fats = self.get_fats()
        fitness = self.get_fitness()
        return "Calories: %.2f%% | Proteins: %.2f | Carbohydrates: %.2f | Fats: %.2f -> %.1f%%" % \
               (calories, proteins, carbohydrates, fats, fitness)
