from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from menus.forms import ProfileForm
import menugen.defaults as default
from menus.models import Recipe, Ingredient, Profile


@login_required
def index(request, ajax=False):
    account = request.user.account
    profile = account.profile
    guests = account.guests.order_by('modified').reverse()
    guests_nb = guests.count()

    if ajax:
        return {
            'user_profile': profile,
            'guests':       guests,
            'guests_nb':    guests_nb,
        }
    return render(request, 'profiles/guests/index.html', {
        'user_profile':     profile,
        'guests':           guests,
        'guests_nb':        guests_nb,
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

def update_physio(request):
    """ This method is used as ajax call in order to update physio """

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    height = request.POST.get('height')
    weight = request.POST.get('weight')
    activity = request.POST.get('activity')
    sex = request.POST.get('sex')
    birthday = request.POST.get('birthday')
    name = request.POST.get('name')
    pk = request.POST.get('pk')

    if request.user.is_authenticated():
        #p = request.user.account.profile
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


def physiology(request, p=None, ajax=False):
    if request.user.is_authenticated():
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
            'name': request.session['name'] if 'name' in request.session else "",
            'sex': request.session.get('sex') if 'sex' in request.session else default.SEX,
            'birthday': request.session['birthday'] if 'birthday' in request.session else "",
            'height': request.session.get('height') if 'height' in request.session else default.HEIGHT,
            'weight': request.session.get('weight') if 'weight' in request.session else default.WEIGHT,
            'activity': request.session.get('activity') if 'activity' in request.session else default.ACTIVITY,
        }

    if ajax:
        return physio
    else:
        return render(request, 'profiles/physiology.html', {
            'physio': physio,
        })


def regimes(request, ajax=False):
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
    r = regimes(request, True)
    g = index(request, True)

    profile_id = int(profile_id) if profile_id != 0 else request.user.account.profile_id
    p = Profile.objects.get(pk=profile_id)
    #p = get_object_or_404(Profile, pk=profile_id)
    # TODO : test propriety

    return render(request, 'profiles/_base.html', {
        'physio':               physiology(request, p, True),
        'health_regimes_list':  r['health_regimes_list'],
        'value_regimes_list':   r['value_regimes_list'],
        'user_profile':         g['user_profile'],
        'guests':               g['guests'],
        'guests_nb':            g['guests_nb'],
        'pk':                   profile_id,
    })


@login_required
def tastes(request):
    profile = request.user.account.profile;
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes.all()
    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes' : unlikes_recipes,
        'unlikes_ingredients' : unlikes_ingredients,
    })


@login_required
def relike_recipe(request, recipe_id):
    profile = request.user.account.profile;
    recipe = Recipe.objects.get(id=recipe_id)
    profile.unlikes_recipe.remove(recipe)
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes.all()
    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes' : unlikes_recipes,
        'unlikes_ingredients' : unlikes_ingredients,
    })


@login_required
def relike_ingredient(request, ingredient_id):
    profile = request.user.account.profile;
    ingredient = Ingredient.objects.get(id=ingredient_id)
    profile.unlikes.remove(ingredient)
    unlikes_recipes = profile.unlikes_recipe.all()
    unlikes_ingredients = profile.unlikes.all()
    return render(request, 'profiles/tastes.html', {
        'unlikes_recipes' : unlikes_recipes,
        'unlikes_ingredients' : unlikes_ingredients,
    })

