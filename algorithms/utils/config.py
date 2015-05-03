__author__ = 'PLNech'


class Config():
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

    KEY_NB_TEST_STEPS = "nb_test_steps"

    parameters = {
        # Sizes
        KEY_POPULATION_SIZE: 100,  # Number of individuals in each generation
        KEY_TOURNAMENT_SIZE: 10,  # Number of random individuals in each tournament

        # Amounts
        KEY_RUN_NUMBER: 1,  # Number of runs
        KEY_NB_GENERATION: 100,  # Number of generations

        # Algorithm parameters
        KEY_ELITISM: True,
        KEY_MUTATION_RATE: 0.15,

        KEY_SOLUTION_TYPE: "Menu",

        # Trip-related parameters
        KEY_CITIES_NUMBER: 30,
        KEY_GRID_SIZE: 200,  # Size of the city position grid

        # Menu-related parameters
        KEY_NB_DISHES: 1000,  # Number of dishes to choose between
        KEY_MAX_DISHES: 7 * 5 * 3,  # Maximum dishes per weekly menu
        KEY_MAX_DISH_CALORIES: 250,  # Maximum amount of calories in a dish
        KEY_MAX_DISH_FATS: 100,  # Maximum amount of grams of fat in a dish
        KEY_MAX_DISH_CARBOHYDRATES: 106,  # Maximum amount of grams of carbohydrates in a dish
        KEY_MAX_DISH_PROTEINS: 50,  # Maximum amount of grams of proteins in a dish TODO Use real value
        KEY_OVERWEIGHT_FACTOR: 1.1,  # Factor of allowed overweight

        KEY_NB_TEST_STEPS: 20,  # Number of test steps
    }

    draw_progress = True  # Should we draw progress of each significative generation?
    draw_results = parameters[KEY_SOLUTION_TYPE] is "Trip"  # Should we draw results of each run?
    draw_all = parameters[KEY_SOLUTION_TYPE] is "Menu"  # Should we draw all steps of each run?

    print_each_run = True  # Should we print results for each run?
    print_generation = True  # Should we print details of each generation?
    print_population = False  # Should we print the generated population?
    print_items = False  # Should we print the randomly generated items ?
    print_selection = False  # Should we print the selection of individuals?
    print_crossover = False  # Should we print the crossover of individuals?
    print_mutation = False  # Should we print the mutation of individuals?

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
    ]
