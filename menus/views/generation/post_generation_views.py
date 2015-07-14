import time

import menugen.defaults as defaults
from django.shortcuts import render
from menus.algorithms.dietetics import Calculator
from menus.algorithms.run import run_standard
from menus.algorithms.utils.config import Config
from menus.data.generator import generate_planning_from_list
from menus.models import Recipe


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

    user_exercise = replace_if_none(request.session.get('exercise'), defaults.EXERCISE)
    user_age = int(replace_if_none(request.session.get('age'), defaults.AGE))
    user_weight = int(replace_if_none(request.session.get('weight'), defaults.WEIGHT))
    user_height = int(float(int(replace_if_none(request.session.get('height'), defaults.HEIGHT)) * 100))
    user_sex = request.session.get('sex')
    user_sex = Calculator.SEX_F if user_sex is 1 else Calculator.SEX_H

    needs = Calculator.estimate_needs(user_age, user_height, user_weight, user_sex, user_exercise)

    # """ Here is an example of a matrix containing (nb_days x 5) meals """
    # planning = generate_planning(nb_days, nb_meals, nb_dishes)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_days * nb_meals * nb_dishes
    Config.update_needs(needs, nb_days)
    menu = run_standard(None, time.ctime())
    planning = generate_planning_from_list(nb_days, nb_meals, menu)

    return render(request, 'menus/generation/generation.html', {'planning': planning, 'days_range': range(0, nb_days)})


def replace_if_none(var, default):
    if var is None:
        var = default
    return var


def generation_meal_details(request, starter_id, main_course_id, dessert_id):
    """ Here should be loaded a meal from db according to the given ids
    A meal is composed of a starter, a main course and a dessert """

    starter = Recipe.objects.get(pk=starter_id)
    main = Recipe.objects.get(pk=main_course_id)
    dessert = Recipe.objects.get(pk=dessert_id)

    meal = {'starter': starter, 'main_course': main, 'dessert': dessert}
    return render(request, 'menus/generation/meal_details.html', {'meal': meal})
