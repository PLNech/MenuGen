import datetime
import logging
import time
from functools import reduce

import numpy
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import menugen.defaults as defaults
from menus.data.generator import generate_planning_from_matrix
from menus.models import Recipe, Ingredient

logger = logging.getLogger("menus")


def generation(request):
    logging.info("Generation!")
    """ Profile values are accessible from current session
        ex:
        WhateverAlgo(request.session['sex'], request.session['age'], request.session['height'], request.session['weight'])
        or
        WhateverAlgo2(request.session['budget'], request.session['difficulty'], request.session['nb_days'])
        """
    from menus.algorithms.dietetics import Calculator
    from menus.models import Profile
    from menus.algorithms.utils.config import Config
    from menus.algorithms.model.menu.menu_manager import MenuManager
    from menus.algorithms.run import run_standard
    from menus.data.generator import generate_planning_from_list

    """ TODO:
    Here should be called the algorithm
    generating the structure containing the meals
    should be passed to the rendered view """

    nb_days = int(request.session.get('nb_days', 7))

    """ Default values """
    nb_dishes = 3
    nb_meals = 2

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        nb_meals_menu = numpy.sum(matrix)
    else:
        nb_meals_menu = nb_meals * nb_days

    today = datetime.date.today()

    user_exercise = request.session.get('exercise', defaults.EXERCISE)
    user_age = int(request.session.get('age', defaults.AGE))
    user_weight = int(request.session.get('weight', defaults.WEIGHT))
    user_height = int(float(request.session.get('height', defaults.HEIGHT / 100)) * 100)
    user_sex = Calculator.SEX_F if request.session.get('sex') is 1 else Calculator.SEX_H
    user_birthday = datetime.date(year=today.year - user_age, month=today.month, day=today.day)

    if request is not None and hasattr(request, 'user') and hasattr(request.user, 'profile'):
        # We have a real user, did it specify profiles?
        if 'profiles' in request.session:
            # Using selected profiles
            profile_list = []
            for profile_str in request.session['profiles']:
                for p in serializers.deserialize("json", profile_str):
                    profile = p.object
                logger.info("Profile found: %s." % profile.name)
                profile_list.append(profile)
            logger.info('Crafted profile list from %d user-selected profiles.' % len(profile_list))
        else:
            # Using only user's profile
            logger.info('Crafted profile list from user profile.')
            profile_list = [request.user.profile]
    else:
        # Using user input or default values
        profile_list = [Profile(weight=user_weight, height=user_height, birthday=user_birthday, sex=user_sex,
                                activity=user_exercise)]
        logger.info('Crafted profile list from request data.')
    logger.info('End of profile choice.')
    logger.info('Profiles at generation: %r.' % profile_list)
    needs_list = [Calculator.estimate_needs_profile(profile) for profile in profile_list]
    needs = reduce(lambda x, y: x + y, needs_list)
    logger.info("Final needs: %r" % needs)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_meals_menu * nb_dishes
    logger.info("Max dishes set to %d." % Config.parameters[Config.KEY_MAX_DISHES])
    Config.update_needs(needs, nb_days)

    # Initialising MenuManager with appropriate meals for profile(s)
    MenuManager.new(profile_list)
    menu = run_standard(run_name=time.ctime())
    if len(menu.genes) < nb_meals_menu:
        pass  # FIXME: Remove after investigation

    if 'matrix' in request.session:
        matrix = request.session['matrix']
        planning = generate_planning_from_matrix(matrix, menu)
    else:
        planning = generate_planning_from_list(nb_days, nb_meals, menu)

    shopping_list = {}
    for meal_time in planning:
        for meal in meal_time:
            if meal:
                main_course = meal['main_course']
                for i in main_course.ingredients.all():
                    try:
                        shopping_list[i.name] += 1
                    except KeyError:
                        shopping_list[i.name] = 1
    request.session['shopping_list'] = shopping_list

    return render(request, 'menus/generation/generation.html', {
        'planning': planning,
        'days_range': range(0, nb_days)
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


def generation_shopping_list(request):
    shopping_list = request.session.get('shopping_list', None)
    return render(request, 'menus/generation/shopping_list.html', {
        'shopping_list': shopping_list
    })


def shopping_list_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_de_courses.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)

    shopping_list = request.session.get('shopping_list', None)
    width, height = letter

    # Draw things on the PDF. Here's where the PDF generation happens.
    p.roundRect(250, height - 120, 200, 50, 20)
    p.drawString(300, height - 100, "Liste de courses")
    i = height - 150
    for ingred, quantity in shopping_list.items():
        p.drawString(100, i, "- " + str(quantity) + " " + ingred)
        i -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


@login_required
def unlike_recipe_message(request, recipe_id):
    """ Message after unliking a recipe """
    recipe = Recipe.objects.get(id=recipe_id)
    profile = request.user.account.profile
    profile.unlikes_recipe.add(recipe)
    return render(request, 'menus/generation/unlike_recipe_popup.html', {
        'recipe_name': recipe.name
    })


@login_required
def unlike_ingredient_message(request, ingredient_id):
    """ Message after unliking an ingredient """
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile = request.user.account.profile
    profile.unlikes_ingredient.add(ingredient)
    return render(request, 'menus/generation/unlike_ingredient_popup.html', {
        'ingredient_name': ingredient.name
    })
