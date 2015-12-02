__author__ = 'PLNech'


class Config:
    KEY_POPULATION_SIZE = "population_size"
    KEY_TOURNAMENT_SIZE = "tournament_size"
    KEY_RUN_NUMBER = "nb_runs"
    KEY_NB_GENERATION = "nb_generations"
    KEY_ELITISM = "elitism"
    KEY_MUTATION_RATE = "mutation_rate"

    KEY_SOLUTION_TYPE = "solution_type"

    KEY_CITIES_NUMBER = "nb_cities"
    KEY_GRID_SIZE = "grid_size"
    KEY_MAX_DISH_CALORIES = "max_dish_calories"
    KEY_MAX_DISH_FATS = "max_dish_fats"
    KEY_MAX_DISH_CARBOHYDRATES = "max_dish_carbohydrates"
    KEY_MAX_DISH_PROTEINS = "max_dish_proteins"
    KEY_OVERWEIGHT_FACTOR = "overweight_factor"
    KEY_NB_DISHES = "nb_dishes"
    KEY_MAX_DISHES = "max_dishes"
    KEY_OBJECTIVE_CALORIES = "calories"
    KEY_OBJECTIVE_PROTEINS_MIN = "min_proteins"
    KEY_OBJECTIVE_PROTEINS_MAX = "max_proteins"
    KEY_OBJECTIVE_CARBOHYDRATES_MIN = "min_carbs"
    KEY_OBJECTIVE_CARBOHYDRATES_MAX = "max_carbs"
    KEY_OBJECTIVE_FATS_MAX = "min_fats"
    KEY_OBJECTIVE_FATS_MIN = "max_fats"

    KEY_NB_TEST_STEPS = "nb_test_steps"

    parameters = {
        # Sizes
        KEY_POPULATION_SIZE: 10,  # Number of individuals in each generation
        KEY_TOURNAMENT_SIZE: 5,  # Number of random individuals in each tournament

        # Amounts
        KEY_RUN_NUMBER: 1,  # Number of runs
        KEY_NB_GENERATION: 100,  # Number of generations

        # Algorithm parameters
        KEY_ELITISM: True,
        KEY_MUTATION_RATE: 0.015,

        KEY_SOLUTION_TYPE: "Menu",  # TODO Get rid of Trip variability

        # Trip-related parameters
        KEY_CITIES_NUMBER: 30,
        KEY_GRID_SIZE: 200,  # Size of the city position grid

        # Menu-related parameters
        KEY_NB_DISHES: 50,  # Number of dishes to choose between
        KEY_MAX_DISHES: 7 * 2 * 3,  # Maximum dishes per weekly menu
        KEY_MAX_DISH_CALORIES: 250,  # Maximum amount of calories in a dish
        KEY_MAX_DISH_FATS: 100,  # Maximum amount of grams of fat in a dish
        KEY_MAX_DISH_CARBOHYDRATES: 106,  # Maximum amount of grams of carbohydrates in a dish
        KEY_MAX_DISH_PROTEINS: 50,  # Maximum amount of grams of proteins in a dish TODO Use real value
        KEY_OVERWEIGHT_FACTOR: 1.1,  # Factor of allowed overweight

        # Optimisation-related parameters
        KEY_OBJECTIVE_CALORIES: 2697.0 * 7,
        KEY_OBJECTIVE_PROTEINS_MIN: 67.4 * 7,
        KEY_OBJECTIVE_PROTEINS_MAX: 236 * 7,
        KEY_OBJECTIVE_CARBOHYDRATES_MIN: 303 * 7,
        KEY_OBJECTIVE_CARBOHYDRATES_MAX: 438 * 7,
        KEY_OBJECTIVE_FATS_MIN: 59.9 * 7,
        KEY_OBJECTIVE_FATS_MAX: 105 * 7,

        KEY_NB_TEST_STEPS: 20,  # Number of test steps
    }

    draw_progress = False  # Should we draw progress of each significative generation?
    draw_results = False  # Should we draw results of each run?
    draw_all = False  # Should we draw all steps of each run?

    print_each_run = False  # Should we print results for each run?
    print_generation = True  # Should we print details of each generation?
    print_population = False  # Should we print the generated population?
    print_selection = False  # Should we print the selection of individuals?
    print_crossover = False  # Should we print the crossover of individuals?
    print_mutation = False  # Should we print the mutation of individuals?
    print_manager = False  # Debug information about the solution manager

    fake_run = False  # Do we care about optimising anything?

    folder_name_output = "img"
    folder_name_log = "log"

    score_dimensions = {
        "Trip": "distance",
        "Menu": "adequacy"
    }

    score_units = {
        "Trip": "km",
        "Menu": ""
    }

    dish_names = [
        "Poulet roti",
        "Céréales",
        "Pizza",
        "Chips",
        "Thé glacé",
        "Chili",
        "Sushis",
        "Soupe miso",
        "Nachos",
        "Quesadilla",
        "Boeuf sauté",
        "Soupe au chou",
        "Salade Océane",
        "Couscous",
        "Tajine",
        "Artichauts grillés",
        "cake aux fruits",
        "confiture allégée abricot",
        "crêpes jambon emmental",
        "espresso",
        "fruitwater",
        "grand chocolat",
        "instant café",
        "la madeleine au beurre frais",
        "les crunchy",
        "marguerites",
        "pommes peches",
        "Boeuf aux lentilles",
        "Boeuf boulgour",
        "Boeuf bourguignon",
        "Boeuf bourguignon",
        "Colin d'Alaska & Crevettes et riz sauce crudités",
        "Colin d'Alaska & légumes et riz sauce citron",
        "Colin d'alaska ail & fines herbes",
        "Colines",
        "Colines ecológicos &quot;BioMonti&quot;",
        "Collection Mousseline - Sir Thomas Lipton",
        "Collection exclusive",
        "Collerettes Cuisson Rapide",
        "Compote Pomme cuite au chaudron",
        "Compote Pomme-poire Bio Monoprix",
        "Compote Pommes Poires Carrefour",
        "Compote Pommes Vanille Carrefour",
        "Compote Pêches Bonne Maman",
        "Compote Pêches Brugnons avec morceaux fondants",
        "Compote Rhubarbe",
        "Compote allégée en sucres Pomme-Poire",
        "Compote allégée pomme banane",
        "Compote allégée pomme figue cannelle",
        "Compote allégée pomme fraise",
        "Compote allégée pomme poire",
        "Compote allégée pomme poire",
        "Compote allégée pomme poire",
        "Compote allégée pomme pêche",
        "Compote avec morceaux & pêche",
        "Compote de Pomme bio allégée en sucres",
        "Compote de Pommes Morceaux",
        "Compote de pomme",
        "Compote de pomme allégée en sucres Bio Monoprix",
        "Galettes bretonnes pur beurre",
        "Galettes bretonnes pur beurre",
        "Galettes bretonnes pur beurre pépites de chocolat Leader Price",
        "Galettes bretonnes pépites de chocolat",
        "Galettes chocolat Gayelord Hauser",
        "Galettes d'épeautre au son d'avoine",
        "Galettes de Céréales aux 2 Fromages Bio",
        "Galettes de Maïs",
        "Galettes de Maïs Bio",
        "Galettes de Maïs Bio extra-fines",
        "Galettes de Maïs au Chocolat Noir Bio",
        "Galettes de Normandie pur beurre",
        "Galettes de Pleyben",
        "Galettes de Riz",
        "Galettes de Riz Bio au Chocolat Noir",
        "Galettes de Riz Complet Bio",
        "Galettes de blé noir bio",
        "Gelato d'Italia Pesca Melba",
        "Gelato d'Italia Pistacchio",
        "Gelbe Orient Linsen",
        "Gelée Bonne Maman Coings",
        "Gelée Bonne Maman Framboises",
        "Gelée Bonne Maman Mûres",
        "Gelée Bonne Maman, Mûres",
        "Gelée Extra Groseilles",
        "Gelée au Madere",
        "Gelée au Madère",
        "Gelée de Marie Jeanne au piment d'Espelette",
        "Gelée de coing",
        "Gelée de mûres framboises",
        "Gelée extra Framboise",
        "Gelée extra de groseilles Leader Price",
        "Gelée extra goyave",
        "Gelée extra groseille",
        "Gelée extra maracudja",
        "Gelée framboise",
        "Gervais a boire",
        "Gervais maxi",
        "Gervais maxi",
        "Gervais maxi",
        "Gervais maxi framboise abricot",
        "Gervais à la vanille",
        "Gervais, fraise, abricot, framboise",
        "Gervita Nature",
        "Gervita Nature (10,3% MG)",
        "Macadamias",
        "Macaron aux framboises",
        "Macaron aux framboises",
        "Macaronade &quot;Fruits de mer&quot;",
        "Macaroni",
        "Macaroni",
        "Macaroni & Cheese",
        ]

    @staticmethod
    def update_needs(needs, nb_days):
        """

        :type needs: menus.algorithms.dietetics.DieteticsNeeds
        :param nb_days: int
        :return:
        """
        Config.parameters[Config.KEY_OBJECTIVE_CALORIES] = needs.calories * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_PROTEINS_MIN] = needs.proteins_min * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_PROTEINS_MAX] = needs.proteins_max * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MIN] = needs.carbs_min * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_CARBOHYDRATES_MAX] = needs.carbs_max * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_FATS_MIN] = needs.fats_min * nb_days
        Config.parameters[Config.KEY_OBJECTIVE_FATS_MAX] = needs.fats_max * nb_days
        print("Dietetic needs set to %s." % needs)
