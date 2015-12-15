import datetime

try:
    import cPickle as pickle
except ImportError:
    import pickle

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

    fake_data_filename = 'response_parameters.dat'
    if Config.fake_run:
        start = time.time()
        logger.info("Fake run. Trying to load fake data...")
        with open(fake_data_filename, 'rb') as f:
            try:
                response_parameters = pickle.load(f)
                logger.info("Got fake data! Returning...")
                elapsed = time.time() - start
                while elapsed < 5:
                    time.sleep(0.5)
                    elapsed = time.time() - start
                return render(request, 'menus/generation/generation.html',
                              response_parameters)
            except Exception as e:
                logger.info("Got an %s while loading fake data: %s" % (type(e), e))

    nb_days = int(request.session.get('nb_days', 7))
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

    if request is not None \
            and hasattr(request, 'user') \
            and hasattr(request.user, 'account') \
            and hasattr(request.user.account, 'profile'):
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
            profile_list = [request.user.account.profile]
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
                    association = main_course.recipetoingredient_set.get_queryset().filter(ingredient=i).get()
                    quantity = association.quantity
                    logger.debug("Shopping list: recipe %s contains %s %s of %s." % (
                        main_course.name, quantity, association.unit, i.name))
                    if i.name in shopping_list:
                        if association.unit in shopping_list[i.name]:
                            shopping_list[i.name]['units'][association.unit] += quantity
                            shopping_list[i.name]['total'] += quantity  # TODO: Consider a coeff to account for unit
                        else:
                            shopping_list[i.name]['units'][association.unit] = quantity
                            shopping_list[i.name]['total'] = quantity
                    else:
                        shopping_list[i.name] = {'name': i.name, 'units': {}, 'total': quantity or 0}
                        shopping_list[i.name]['units'][association.unit] = quantity
    request.session['shopping_list'] = shopping_list

    # stats + pics
    recipes = []
    pics = []
    for meal_time in planning:
        for meal in meal_time:
            if meal:
                starter = meal['starter']
                recipes.append(starter)
                if starter.picture:
                    pics.append(starter.picture)
                main_course = meal['main_course']
                recipes.append(main_course)
                if main_course.picture:
                    pics.append(main_course.picture)
                dessert = meal['dessert']
                recipes.append(dessert)
                if dessert.picture:
                    pics.append(dessert.picture)

    response_parameters = {'planning': planning, 'days_range': range(0, nb_days),
                           'nb_very_easy': len([r for r in recipes if r.difficulty == 0]),
                           'nb_easy': len([r for r in recipes if r.difficulty == 1]),
                           'nb_medium': len([r for r in recipes if r.difficulty == 2]),
                           'nb_difficult': len([r for r in recipes if r.difficulty == 3]),
                           'cat_amuse_gueule': len([r for r in recipes if r.category == 'Amuse-gueule']),
                           'cat_confiserie': len([r for r in recipes if r.category == 'Confiserie']),
                           'cat_conseil': len([r for r in recipes if r.category == 'Conseil']),
                           'cat_accompagnement': len([r for r in recipes if r.category == 'Accompagnement']),
                           'cat_dessert': len([r for r in recipes if r.category == 'Dessert']),
                           'cat_entree': len([r for r in recipes if r.category == 'Entrée']),
                           'cat_sauce': len([r for r in recipes if r.category == 'Sauce']),
                           'cat_boisson': len([r for r in recipes if r.category == 'Boisson']),
                           'cat_plat_principal': len([r for r in recipes if r.category == 'Plat principal']),
                           'price_0': len([r for r in recipes if r.price == 0]),
                           'price_1': len([r for r in recipes if r.price == 1]),
                           'price_2': len([r for r in recipes if r.price == 2]), 'pics': pics}
    with open(fake_data_filename, 'wb') as f:
        pickle.dump(response_parameters, f)
        logger.info("Saved new stored_data.")

    http_response = render(request, 'menus/generation/generation.html', response_parameters)
    return http_response


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

def recipe_pics(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    return render(request, 'menus/recipe_pic.html', {
        'recipe': recipe
    })
