from datetime import datetime
import logging

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect

from django.shortcuts import render, redirect, get_object_or_404

from menus.forms import ProfileForm
import menugen.defaults as default
from menus.models import Recipe, Ingredient, Profile, Diet
from menus.utils import json2obj

logger = logging.getLogger("menus")

@login_required
def index(request, ajax=False):
    account = request.user.account
    profile = account.profile
    guests = account.guests.order_by('modified').reverse()
    guests_nb = guests.count()

    if ajax:
        return {
            'user_profile': profile,
            'guests': guests,
            'guests_nb': guests_nb,
        }
    return render(request, 'profiles/guests/index.html', {
        'user_profile': profile,
        'guests': guests,
        'guests_nb': guests_nb,
    })


@login_required
def new(request):
    if request.method == 'GET':
        form = ProfileForm
        return render(request, 'profiles/guests/new_modal.html', {'form': form})
    else:
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            profile = form.profile_cache
            profile.save()
            account = request.user.account
            account.guests.add(profile)
            return render(request, 'profiles/guests/guest.html', {
                'profile': profile
            })

        return HttpResponse(content=render(request, 'profiles/guests/new_modal.html', {'form': form}),
                            content_type='text/html; charset=utf-8',
                            status=form.error_code)


@login_required
def detail(request, profile_id):
    account = request.user.account
    p = account.guests.get(id__exact=profile_id)
    return render(request, 'profiles/guests/detail.html', {
        'profile': p
    })


@login_required
def edit(request, profile_id):
    print(profile_id)
    # return render(request, 'profiles/guests/edit.html')
    return redirect('physiology')


@login_required
def remove(request, profile_id):
    account = request.user.account
    p = account.guests.filter(id__exact=profile_id).first()
    # TODO : check ownership
    if request.method == 'GET':
        title = 'Suppression du profile ' + p.name
        message = 'Etes vous certain de vouloir supprimer ce profile ?'
        action = 'Supprimer'

        return render(request, 'profiles/guests/remove_modal.html', {
            'profile': p,
            'title': title,
            'message': message,
            'action': action
        })
    else:
        p.delete()
        return HttpResponseRedirect('/profile')


def update_profile(request):
    """ This method is used as ajax call in order to update user profile """

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    height = request.POST.get('height')
    weight = request.POST.get('weight')
    activity = request.POST.get('activity')
    sex = request.POST.get('sex')
    birthday = request.POST.get('birthday')
    name = request.POST.get('name')
    pk = request.POST.get('pk')
    diets = request.POST.get('diets')

    if request.user.is_authenticated():
        # p = request.user.account.profile
        p = get_object_or_404(Profile, pk=pk)
        # TODO : check propriety
        if name:
            p.name = name
        elif sex:
            p.sex = sex
        elif birthday:
            p.birthday = datetime.strptime(birthday, '%d-%m-%Y') if len(birthday) else datetime.now()
        elif height:
            p.height = height
        elif weight:
            p.weight = weight
        elif activity:
            p.activity = activity
        elif diets:
            diets = json2obj(diets)

            for key, checked in diets:
                if Diet.objects.filter(pk=key).exists():
                    if checked:
                        p.diets.add(key)
                    else:
                        p.diets.remove(key)
        p.save()

    else:
        if name:
            request.session['name'] = name
        elif birthday:
            request.session['birthday'] = birthday
        elif sex:
            request.session['sex'] = sex
        elif height:
            request.session['height'] = height
        elif weight:
            request.session['weight'] = weight
        elif activity:
            request.session['activity'] = activity
        elif diets:
            request.session['activity'] = activity

    return HttpResponse(diets)


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


def physiology(request, p=None, ajax=False):
    if request.user.is_authenticated() and p is not None:
        physio = {
            'name': p.name,
            'sex': p.sex,
            'birthday': p.birthday.strftime('%d-%m-%Y'),
            'height': p.height,
            'weight': p.weight,
            'activity': p.activity,
        }

    else:
        physio = {
            'name': request.session.get('name', default.NAME),
            'sex': request.session.get('sex', default.SEX),
            'birthday': request.session.get('birthday', default.BIRTHDAY),
            'height': request.session.get('height', default.HEIGHT),
            'weight': request.session.get('weight', default.WEIGHT),
            'activity': request.session.get('activity', default.ACTIVITY),
        }

    if ajax:
        return physio
    else:
        return render(request, 'profiles/physiology.html', {
            'physio': physio,
        })


def regimes(request, ajax=False, profile_id=None):
    vege_diets = Diet.objects.filter(name__startswith='Végé')
    health_regimes_list = []
    value_regimes_list = []
    profile = Profile.objects.get(pk=profile_id)
    logger.info("Generating profile view for %s, given %d." % (profile.name, int(profile_id)))

    for diet in vege_diets:
        diet.active = profile.diets.filter(pk=diet.pk).exists()
        value_regimes_list.append(diet)

    regime_hyper_prot = {
        'name': 'Hyperprotéiné',
        'description': "Régime amaigrissant fondé sur l'absorption de protéines aussi pures que possibles. Ce régime est fortement hypocalorique.",
        'pk': -1,
        'active': False
    }
    regime_sans_gluten = {
        'name': 'Sans gluten',
        'description': "Préconisé dans le cas de l'intolérance au gluten, ce régime permet d'éviter une réaction immunitaire à la gliadine.",
        'pk': -2,
        'active': False
    }

    health_regimes_list.append(regime_hyper_prot)
    health_regimes_list.append(regime_sans_gluten)

    if ajax:
        return {
            'health_regimes_list': health_regimes_list,
            'value_regimes_list': value_regimes_list
        }
    else:
        return render(request, 'profiles/regimes.html', {
            'health_regimes_list': health_regimes_list,
            'value_regimes_list': value_regimes_list
        })


@login_required
def profile(request, profile_id=0):
    profile_id = int(profile_id) if profile_id != 0 else request.user.account.profile_id

    r = regimes(request, True, profile_id=profile_id)
    g = index(request, True)
    p = Profile.objects.get(pk=profile_id)
    # p = get_object_or_404(Profile, pk=profile_id)
    # TODO : test propriety

    return render(request, 'profiles/_base.html', {
        'physio': physiology(request, p, True),
        'health_regimes_list': r['health_regimes_list'],
        'value_regimes_list': r['value_regimes_list'],
        'profile': p,
        'user_profile': g['user_profile'],
        'guests': g['guests'],
        'guests_nb': g['guests_nb'],
        'pk': profile_id,
    })


@login_required
def tastes(request):
    profile = request.user.account.profile
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes_ingredient.all()

    found_recipes = None
    found_ingredients = None
    if 'query' in request.POST and request.POST['query']:
        found_recipes = Recipe.objects.filter(name__icontains=request.POST['query'])
        found_ingredients = Ingredient.objects.filter(name__icontains=request.POST['query'])

    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes': unlikes_recipes,
        'unlikes_ingredients': unlikes_ingredients,
        'found_recipes': found_recipes,
        'found_ingredients': found_ingredients
    })


@login_required
def relike_recipe(request, recipe_id):
    profile = request.user.account.profile
    recipe = Recipe.objects.get(id=recipe_id)
    profile.unlikes_recipe.remove(recipe)
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes_ingredient.all()
    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes': unlikes_recipes,
        'unlikes_ingredients': unlikes_ingredients,
    })


@login_required
def relike_ingredient(request, ingredient_id):
    profile = request.user.account.profile
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile.unlikes_ingredient.remove(ingredient)
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes_ingredient.all()
    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes': unlikes_recipes,
        'unlikes_ingredients': unlikes_ingredients,
    })

@login_required
def unlike_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    profile = request.user.account.profile;
    profile.unlikes_recipe.add(recipe);

    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes_ingredient.all()

    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes': unlikes_recipes,
        'unlikes_ingredients': unlikes_ingredients,
    })


@login_required
def unlike_ingredient(request, ingredient_id):
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile = request.user.account.profile;
    profile.unlikes_ingredient.add(ingredient)

    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes_ingredient.all()

    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes': unlikes_recipes,
        'unlikes_ingredients': unlikes_ingredients,
    })
