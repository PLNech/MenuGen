from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from menus.models import Recipe


def landing(request):
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

    starter = Recipe()
    starter.id = 0
    starter.name = "Petit déjeuner"
    starter.prep_time = 5
    starter.cook_time = 10
    starter.difficulty = 2
    starter.price = 2

    main = Recipe()
    main.id = 1
    main.name = "Plat principale"
    main.prep_time = 5
    main.cook_time = 20
    main.difficulty = 3
    main.price = 3

    dessert = Recipe()
    dessert.id = 2
    dessert.name = "Dessert"
    dessert.prep_time = 5
    dessert.cook_time = 0
    dessert.difficulty = 2
    dessert.price = 2

    """ Default days number """
    nb_days = 7
    """ Use the days number if exists """
    if 'nb_days' in request.session:
        nb_days = int(request.session['nb_days'])

    """ Here is an example of meal"""
    meal = {'starter': starter, 'main_course': main, 'dessert': dessert}

    """ Here is an example of a matrix containing (nb_days x 5) meals """
    planning = [[meal for y in range(nb_days)] for x in range(5)]

    return render(request, 'menus/generation/generation.html', {'planning': planning, 'days_range': range(0, nb_days)})


def generation_meal_details(request, starter_id, main_course_id, dessert_id):
    """ Here should be load a meal from db according to the given ids
    A meal is composed of a starter, a main course and a dessert """
    starter = Recipe()
    starter.id = starter_id
    starter.name = "Un petit déjeuner"
    starter.prep_time = 5
    starter.cook_time = 10
    starter.difficulty = 2
    starter.price = 2

    main = Recipe()
    main.id = main_course_id
    main.name = "Un plat principale"
    main.prep_time = 5
    main.cook_time = 20
    main.difficulty = 3
    main.price = 3

    dessert = Recipe()
    dessert.id = dessert_id
    dessert.name = "Un dessert"
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
        return render(request, 'profile/physiology.html', {'current_physio': request.session, 'ages': range(5, 151)})


def regimes(request):
    return render(request, 'profile/regimes.html', {})


def tastes(request):
    return render(request, 'profile/tastes.html', {})


@login_required
def account(request):
    return render(request, 'profile/account.html', {})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('menus.views.friends')
            else:
                return render(request, 'auth/sign_in.html', {})
        else:
            return render(request, 'auth/sign_in.html', {})
    else:
        return render(request, 'auth/sign_in.html', {})


def sign_up(request):
    return render(request, 'auth/sign_up.html', {})


@login_required
def sign_out(request):
    logout(request)
    return redirect('menus.views.landing')
