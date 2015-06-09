import time
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from menus.algorithms.dietetics import Calculator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from menus.data.generator import generate_planning
from menus.models import Recipe
from menus.models import Ingredient
from menus.algorithms.run import run_standard
from menus.algorithms.utils.config import Config


def landing(request):
    request.session.flush()
    # if 'liked_aliments' not in request.session:
    # request.session['liked_aliments'] = ["Eau", "Chocolat", "Tagliatelles", "Dinde", "Poulet", "Boeuf", "Jambon", "Sucre", "Semoule", "Riz", "Spaghetti", "Lasagnes", "Framboise", "Fraise", "Cerise", "Groseille", "Pomme", "Poire", "Ananas", "Courgette", "Carotte", "Aubergine", "Tomate", "Radis", "Lait", "Oeuf", "Myrtille", "Farine", "Abricot", "Ail", "Oignon", "Saumon", "Beurre", "Fromage", "Fruits", "Légumes", "Viande", "Poisson", "Menthe", "Thym", "Huile de tournesol", "Basilique", "Petits pois", "Haricots verts" ]
    # if 'disliked_aliments' not in request.session:
    #     request.session['disliked_aliments'] = []

    return render(request, 'landing.html', {
        'landing': True})


def home(request):
    return render(request, 'menus/home.html', {})


def generate(request):
    return render(request, 'menus/generate/generate.html',
                  {'days_range': range(0, 7)})


def generate_select_profile(request):
    return render(request, 'menus/generate/select_profile.html', {})


def generate_placements_detail(request):
    nb_days = int(request.POST['nb_days'])
    return render(request, 'menus/generate/placements_detail.html',
                  {'days_range': range(0, nb_days)})


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
    nb_meals = 5  # TODO: Get amount of meals  # FIXME: Differentiate breakfast/lunch/dinner/etc
    nb_dishes = 3  # TODO: Determine appropriate amount for meals ?

    user_exercise = Calculator.EXERCISE_MODERATE  # TODO: Get exercise of user
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

    # needs = Calculator.estimate_needs(user_age, user_height, user_weight, user_sex, user_exercise)

    # """ Here is an example of a matrix containing (nb_days x 5) meals """
    planning = generate_planning(nb_days, nb_meals, nb_dishes)

    Config.parameters[Config.KEY_MAX_DISHES] = nb_days * nb_meals * nb_dishes
    menu = run_standard(None, time.ctime())
    menu_str = ""
    for g in menu.genes:
        menu_str += g.name + "\n"
    print("Result planning:" + menu_str)

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


@login_required
def menus(request):
    return render(request, 'menus/menus.html', {})


@login_required
def friends(request):
    return render(request, 'menus/friends.html', {})


@login_required
def statistics(request):
    return render(request, 'menus/statistics.html', {})


def update_physio(request):
    """ This method is used as ajax call in order to update physio """

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if 'sex' in request.POST:
        request.session['sex'] = request.POST.get('sex')
    if 'age' in request.POST:
        request.session['age'] = request.POST.get('age')
    if 'height' in request.POST:
        request.session['height'] = request.POST.get('height')
    if 'weight' in request.POST:
        request.session['weight'] = request.POST.get('weight')

    return HttpResponse('ok')


def update_gen_criteria(request):
    """ This method is used as ajax call in order to update the pre-generation """
    """ TODO: Handle the matrice of days"""

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if 'budget' in request.POST:
        request.session['budget'] = request.POST.get('budget')
    if 'difficulty' in request.POST:
        request.session['difficulty'] = request.POST.get('difficulty')
    if 'nb_days' in request.POST:
        request.session['nb_days'] = request.POST.get('nb_days')
    print(request.session.items())
    return HttpResponse('ok')


def update_tastes(request):
    """ This method is used as ajax call in order to update physio """

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    # if 'liked' in request.POST:
    # request.session['liked_aliments'].append(request.POST.get('liked'))
    # if 'disliked' in request.POST:
    #     l = request.session['disliked_aliments']
    #     print(l)
    #     print(request.POST.get('disliked'))
    #     request.session['disliked_aliments'] = l.append(request.POST.get('disliked'))
    #
    # print(request.POST)
    # print(request.session['disliked_aliments'])

    return HttpResponse('tastes updated successfully')


def physiology(request):
    if request.method == 'POST':
        username = request.POST['username']
        sex = request.POST['sex']
        height = request.POST['height']
        weight = request.POST['weight']
    else:
        """ TODO:
        - Use current_physio in template to pre-fill profile information.
        - Add ranges for to fill the select tag in template (refer to ages ?) """
        return render(request, 'profile/physiology.html', {'current_physio': request.session})


def regimes(request):
    health_regimes_list = []
    value_regimes_list = []
    nutrients_regimes_st = []
    regime_sans_sel = {
        'name': 'Hyposodé (sans sel)',
        'desc': "Régime pour restreindre le plus possible les apports en sel dans l'alimentation."
    }
    regime_hyper_prot = {
        'name': 'Hyperprotéiné',
        'desc': "Régime amaigrissant fondé sur l'absorption de protéines aussi pures que possibles. Ce régime est fortement hypocalorique."
    }
    regime_sans_gluten = {
        'name': 'Sans gluten',
        'desc': "Préconisé dans le cas de l'intolérance au gluten, ce régime permet d'éviter une réaction immunitaire à la gliadine."
    }
    regime_vegetarien = {
        'name': 'Végétarien',
        'desc': "Régime sans chair animale ni sous-produits d'animaux abattus."
    }
    regime_vegetalien = {
        'name': 'Végétalien',
        'desc': "Régime végétarien excluant également le lait, les œufs, le miel ainsi que leurs dérivés."
    }
    regime_halal = {
        'name': 'Halal',
        'desc': "Régime religieux impliquant l'interdiction de certains aliments."
    }

    health_regimes_list.append(regime_sans_sel)
    health_regimes_list.append(regime_hyper_prot)
    health_regimes_list.append(regime_sans_gluten)
    value_regimes_list.append(regime_vegetarien)
    value_regimes_list.append(regime_vegetalien)
    value_regimes_list.append(regime_halal)
    return render(request, 'profile/regimes.html',
                  {'health_regimes_list': health_regimes_list,
                   'value_regimes_list': value_regimes_list})


def tastes(request):
    return render(request, 'profile/tastes.html',
            { 'ingredients': [ingredient.name for ingredient in Ingredient.objects.all()] })


@login_required
def account(request):
    return render(request, 'profile/account.html', {})


# def sign_in(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('menus.views.friends')
#             else:
#                 return render(request, 'auth/sign_in.html', {})
#         else:
#             return render(request, 'auth/sign_in.html', {})
#     else:
#         return render(request, 'auth/sign_in.html', {})

from menus.forms import RegistrationForm, SignInForm

def sign_in(request):
    if request.method == "GET":
        form = SignInForm
        return render(request, 'auth/sign_in.html', {'form': form})
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        print("here")
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('menus.views.friends')
        return HttpResponse(content=render(request, 'auth/sign_in.html', {'form': form}),
                                content_type='text/html; charset=utf-8',
                                status=403)


def sign_up(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'auth/sign_up.html', {'form': form})
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(False)
            user.set_password(user.password)
            user.save()
            user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, user)

            return redirect('/')
        return render(request, 'auth/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    logout(request)
    return redirect('menus.views.landing')

