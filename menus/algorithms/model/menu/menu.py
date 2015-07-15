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
            objective_calories = Config.parameters[Config.KEY_OBJECTIVE_CALORIES]
            obj_proteins_min = Config.parameters[Config.KEY_OBJECTIVE_PROTEINS_MIN]
            obj_proteins_max = Config.parameters[Config.KEY_OBJECTIVE_PROTEINS_MAX]
            obj_carbs_min = Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MIN]
            obj_carbs_max = Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MAX]
            obj_fats_min = Config.parameters[Config.KEY_OBJECTIVE_FATS_MIN]
            obj_fats_max = Config.parameters[Config.KEY_OBJECTIVE_FATS_MAX]
        else:
            objective_calories = objectives.calories
            obj_proteins_min = objectives.proteins_min
            obj_proteins_max = objectives.proteins_max
            obj_carbs_min = Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MIN]
            obj_carbs_max = Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MAX]
            obj_fats_min = Config.parameters[Config.KEY_OBJECTIVE_FATS_MIN]
            obj_fats_max = Config.parameters[Config.KEY_OBJECTIVE_FATS_MAX]

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
        self.fitness_proteins = self.nutrient_fitness_range(accu_proteins, obj_proteins_min, obj_proteins_max)
        self.fitness_carbohydrates = self.nutrient_fitness_range(accu_carbs, obj_carbs_min, obj_carbs_max)
        self.fitness_fats = self.nutrient_fitness_range(accu_fats, obj_fats_min, obj_fats_max)
        self.fitness = (1 + self.fitness_proteins + self.fitness_carbohydrates + self.fitness_fats) / 4 \
                       * self.fitness_calories
        print("Fitness: %i prot, %i carb, %i fats, %f cal -> %f total." % (self.fitness_proteins, self.fitness_carbohydrates,
                                                  self.fitness_fats, self.fitness_calories, self.fitness))
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
    def nutrient_fitness(quantity, objective):
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

    @staticmethod
    def nutrient_fitness_range(quantity, objective_min, objective_max):
        if objective_min <= quantity <= objective_max:
            return 1
        return 0

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
