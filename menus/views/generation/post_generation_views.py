import datetime
import numpy

from django.contrib.auth.decorators import login_required
from functools import reduce
import time

import menugen.defaults as defaults
from django.shortcuts import render
from menus.algorithms.dietetics import Calculator
from menus.algorithms.run import run_standard
from menus.algorithms.utils.config import Config
from menus.data.generator import generate_planning_from_list, generate_planning_from_matrix
from menus.models import Recipe, Profile, Ingredient


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

    """ Default values """
    nb_dishes = 3
    nb_meals = 2

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        nb_meals_menu = numpy.sum(matrix)
    else:
        nb_meals_menu = nb_meals * nb_days

    today = datetime.date.today()

    user_exercise = replace_if_none(request.session.get('exercise'), defaults.EXERCISE)
    user_age = int(replace_if_none(request.session.get('age'), defaults.AGE))
    user_weight = int(replace_if_none(request.session.get('weight'), defaults.WEIGHT))
    user_height = int(float(int(replace_if_none(request.session.get('height'), defaults.HEIGHT)) * 100))
    user_sex = Calculator.SEX_F if request.session.get('sex') is 1 else Calculator.SEX_H
    user_birthday = datetime.date(year=today.year - user_age, month=today.month, day=today.day)

    profile = Profile(weight=user_weight, height=user_height, birthday=user_birthday, sex=user_sex, activity=user_exercise)
    profile_list = [profile, Profile(weight=100, height=200, birthday=datetime.date(1928, 2, 10),
                                     sex=defaults.SEX, activity=defaults.EXERCISE)]
    # profile_list = [profile]  # TODO: GET list of profiles to 'merge'
    needs_list = [Calculator.estimate_needs_profile(profile) for profile in profile_list]
    needs = reduce(lambda x, y: x+y, needs_list)
    print("Final needs:", needs)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_meals_menu * nb_dishes
    Config.update_needs(needs, nb_days)
    menu = run_standard(None, time.ctime())

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        planning = generate_planning_from_matrix(matrix, menu)
    else:
        planning = generate_planning_from_list(nb_days, nb_meals, menu)

    shopping_list = []
    for meal_time in planning:
        for meal in meal_time:
            if meal:
                print(meal)
                main_course = meal['main_course']
                for i in main_course.ingredients.all():
                    shopping_list.append(i.name)

    return render(request, 'menus/generation/generation.html', {
        'planning': planning,
        'days_range': range(0, nb_days),
        'shopping_list': shopping_list
    })


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


@login_required
def unlike_recipe_message(request, recipe_id):
    """ Message after unliking a recipe """
    recipe = Recipe.objects.get(id=recipe_id)
    profile = request.user.account.profile;
    profile.unlikes_recipe.add(recipe);
    return render(request, 'menus/generation/unlike_recipe_popup.html', {
        'recipe_name': recipe.name
    })


@login_required
def unlike_ingredient_message(request, ingredient_id):
    """ Message after unliking an ingredient """
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile = request.user.account.profile;
    profile.unlikes.add(ingredient)
    return render(request, 'menus/generation/unlike_ingredient_popup.html', {
        'ingredient_name': ingredient.name
    })
