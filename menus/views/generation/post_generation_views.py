import time

from django.shortcuts import render
from menus.algorithms.dietetics import Calculator
from menus.algorithms.run import run_standard
from menus.algorithms.utils.config import Config
from menus.data.generator import generate_planning_from_list
from menus.models import Recipe

__author__ = 'kiyoakimenager'


def generation(request):
    """ Profile values are accessible from current session
        ex:
        WhateverAlgo(request.session['sex'], request.session['age'], request.session['height'], request.session['weight'])
        or
        WhateverAlgo2(request.session['budget'], request.session['difficulty'], request.session['nb_days'])
        """

    """ TODO:
    Here should be called the algorithm
    generating the structure containing the meals
    should be passed to the rendered view """

    """ Default days number """
    nb_days = 7
    """ Use the days number if exists """
    if 'nb_days' in request.session:
        nb_days = int(request.session['nb_days'])
    nb_meals = 3  # TODO: Get amount of meals  # FIXME: Differentiate breakfast/lunch/dinner/etc
    nb_dishes = 3  # TODO: Determine appropriate amount for meals ?

    if 'activity' in request.session:
        user_exercise = request.session['exercise']
    else:
        user_exercise = Calculator.EXERCISE_MODERATE

    if 'age' in request.session:
        user_age = int(request.session['age'])
    else:
        user_age = 20

    if 'height' in request.session:
        user_height = int(float(request.session['height']) * 100)
    else:
        user_height = 180

    if 'weight' in request.session:
        user_weight = int(request.session['weight'])
    else:
        user_weight = 75

    if 'sex' in request.session:
        user_sex = request.session['sex']
    else:
        user_sex = Calculator.SEX_H

    needs = Calculator.estimate_needs(user_age, user_height, user_weight, user_sex, user_exercise)

    # """ Here is an example of a matrix containing (nb_days x 5) meals """
    # planning = generate_planning(nb_days, nb_meals, nb_dishes)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_days * nb_meals * nb_dishes
    Config.update_needs(needs, nb_days)
    menu = run_standard(None, time.ctime())
    planning = generate_planning_from_list(nb_days, nb_meals, menu)

    return render(request, 'menus/generation/generation.html', {'planning': planning, 'days_range': range(0, nb_days)})


def generation_meal_details(request, starter_id, main_course_id, dessert_id):
    """ Here should be load a meal from db according to the given ids
    A meal is composed of a starter, a main course and a dessert """
    starter = Recipe()
    starter.id = starter_id
    starter.name = "Entrée"
    starter.prep_time = 5
    starter.cook_time = 10
    starter.difficulty = 2
    starter.price = 2

    main = Recipe()
    main.id = main_course_id
    main.name = "Plat principal"
    main.prep_time = 5
    main.cook_time = 20
    main.difficulty = 3
    main.price = 3

    dessert = Recipe()
    dessert.id = dessert_id
    dessert.name = "Dessert"
    dessert.prep_time = 5
    dessert.cook_time = 0
    dessert.difficulty = 2
    dessert.price = 2

    meal = {'starter': starter, 'main_course': main, 'dessert': dessert}
    return render(request, 'menus/generation/meal_details.html', {'meal': meal})
