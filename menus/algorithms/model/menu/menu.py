import logging
from random import shuffle

from django.core.cache import cache

from menus.algorithms.dietetics import DieteticsNeeds
from menus.algorithms.model.individual import Individual
from menus.algorithms.model.menu.dish import Dish
from menus.algorithms.model.menu.menu_manager import MenuManager
from menus.algorithms.utils.config import Config
from menus.algorithms.utils.decorators import memoize

__author__ = 'PLNech'
logger = logging.getLogger("menus")


class Menu(Individual):  # TODO Document!
    # noinspection PyMissingConstructor
    # The parent constructor raises an exception as being abstract
    def __init__(self, genes=None):
        if genes is not None:
            self.genes = genes
        else:
            self.genes = []

        self.fitness_variety = 0
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
        ret_str = "[%i|" % len(self.genes)
        for dish in self.genes:
            ret_str += str(dish)
        return ret_str + "]"

    def __repr__(self):
        return "Menu" + str(self)

    def reset_fitness(self):
        self.fitness = 0
        self.fitness_calories = 0
        self.fitness_proteins = 0
        self.fitness_carbohydrates = 0
        self.fitness_fats = 0

    def reset_nutrients(self):
        self.calories = 0
        self.proteins = 0
        self.carbohydrates = 0
        self.fats = 0

        self.genes = []

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
        dish_map = dict()
        for dish in self.genes:
            dish_map[str(dish)] = dish
            accu_calories += dish.calories
            accu_proteins += dish.proteins
            accu_carbs += dish.carbohydrates
            accu_fats += dish.fats

        count_genes = len(self.genes)

        self.fitness_variety = len(dish_map) / count_genes

        self.calories = accu_calories
        self.proteins = accu_proteins
        self.carbohydrates = accu_carbs
        self.fats = accu_fats

        self.fitness_calories = self.nutrient_fitness(accu_calories, objective_calories)
        self.fitness_proteins = self.nutrient_fitness_range(accu_proteins, obj_proteins_min, obj_proteins_max)
        self.fitness_carbohydrates = self.nutrient_fitness_range(accu_carbs, obj_carbs_min, obj_carbs_max)
        self.fitness_fats = self.nutrient_fitness_range(accu_fats, obj_fats_min, obj_fats_max)

        fitness_nutrition = (1 + self.fitness_proteins + self.fitness_carbohydrates + self.fitness_fats) / 4

        fitness_amount = min(count_genes / Config.parameters[Config.KEY_MAX_DISHES],
                             Config.parameters[Config.KEY_MAX_DISHES] / count_genes)

        self.fitness = (fitness_nutrition ** 2) * fitness_amount * self.fitness_calories * self.fitness_variety
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
        self.reset_fitness()

    def generate(self):
        """
        Generates genes from MenuManager dishes
        :return: True if the generation was successful
        :rtype bool
        """
        self.genes = []

        accu_calories = 0
        genes_length = Config.parameters[Config.KEY_MAX_DISHES]

        objective_calories = Config.parameters[Config.KEY_OBJECTIVE_CALORIES]
        over_size = objective_calories * Config.parameters[Config.KEY_OVERWEIGHT_FACTOR]

        init_dishes, available_dishes, ordered_dishes = self.initialise_dishes(objective_calories)
        init_dishes = init_dishes.copy()
        available_dishes = available_dishes.copy()
        ordered_dishes = ordered_dishes.copy()

        for _ in range(genes_length):
            did_used_ordered = False  # Did we use ordered list ? (if yes, it is useless to try the next smallest)
            try:
                dish = available_dishes.pop()
            except IndexError:
                return self.gen_error("No more dishes, and we didn't fill all genes... Generation failed.")
            while accu_calories + dish.calories > over_size:
                logger.debug("Dish too calorific (%d + %d = %d > %d)! Let's try a small one..." %
                             (accu_calories, dish.calories, accu_calories + dish.calories, over_size))
                if len(available_dishes) is 0:
                    return self.gen_error("No more dish available, and we need a smaller one... Generation failed.")
                if did_used_ordered:
                    logger.debug("Smallest dish was too big. "
                                 "Let's remove meal's biggest dish and add two small ones instead...")
                    # No more small dishes, remove biggest and start again adding dishes!

                    # Reset ordered dishes
                    did_used_ordered = False
                    ordered_dishes = sorted(init_dishes, key=lambda x: x.calories, reverse=True)

                    # Get biggest dish in menu
                    max_cal = 0
                    max_gene = None
                    for g in self.genes:
                        if g.calories > max_cal:
                            max_cal = g.calories
                            max_gene = g
                    # Remove it
                    self.genes.remove(max_gene)
                    accu_calories -= max_cal

                    # Add a small one instead
                    smallest = ordered_dishes.pop()
                    self.genes.append(smallest)
                    accu_calories += smallest.calories

                    # Then select a small dish to use as valid dish for this iteration
                    dish = ordered_dishes.pop()
                else:
                    try:
                        dish = ordered_dishes.pop()
                        did_used_ordered = True
                    except IndexError:
                        try:
                            dish = available_dishes.pop()
                            did_used_ordered = False
                        except IndexError:
                            return self.gen_error("Not enough dishes while popping... Generation failed.")
                    logger.debug("Using smallest dish: %d." % dish.calories)

            # Now we have a valid dish, let's add it
            accu_calories += dish.calories
            self.genes.append(dish)

            # Finally don't forget to remove it from the other list too.
            try:
                available_dishes.remove(dish)
                ordered_dishes.remove(dish)
            except ValueError:
                pass

        logger.debug("Finished generating a menu of %d calories through %d dishes." % (accu_calories, len(self.genes)))
        return True

    @staticmethod
    def gen_error(msg):
        logger.error(msg)
        return False

    def initialise_dishes(self, objective_calories, manager=MenuManager.get()):
        if cache.get('did_init_dishes', False):
            init_dishes = cache.get('init_dishes', [])
            available_dishes = cache.get('available_dishes', [])
            ordered_dishes = cache.get('ordered_dishes', [])
            logger.info("Recovered dishes lists from cache.")
        else:
            init_dishes = [dish for dish in manager.dishes[:] if dish.calories <= 0.8 * objective_calories]
            available_dishes = init_dishes
            shuffle(available_dishes)
            ordered_dishes = sorted(available_dishes, key=lambda x: x.calories, reverse=True)

            cache.set('init_dishes', init_dishes)
            cache.set('available_dishes', available_dishes)
            cache.set('ordered_dishes', ordered_dishes)
            logger.info("Initialised dishes lists for menu generation.")

        return init_dishes, available_dishes, ordered_dishes

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
