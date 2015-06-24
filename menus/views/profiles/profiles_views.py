from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

__author__ = 'kiyoakimenager'

@login_required
def friends(request):
    guests = []
    guest_1 = {
        'username': 'Kevin',
        'imc': 20.2
    }
    guest_2 = {
        'username': 'Paul louis',
        'imc': 18
    }
    guest_3 = {
        'username': 'Guillaume',
        'imc': 25
    }
    guests.append(guest_1)
    guests.append(guest_2)
    guests.append(guest_3)
    return render(request, 'profiles/guests/guests.html', {'guests': guests})


@login_required
def profile_infos(request):
    return render(request, 'profiles/guests/guest_infos.html')


def update_physio(request):
    """ This method is used as ajax call in order to update physio """

    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if request.user.is_authenticated():
        p = request.user.owner
        if 'name' in request.POST:
            p.name = int(request.POST['sex'])
        if 'sex' in request.POST:
            p.sex = int(request.POST['sex'])
        if 'birthday' in request.POST:
            p.birthday = request.POST['birthday']
        if 'height' in request.POST:
            p.height = request.POST['height']
        if 'weight' in request.POST:
            p.weight = request.POST['weight']
        if 'activity' in request.POST:
            p.activity = request.POST['activity']
        p.save()

    else:
        if 'name' in request.POST:
            request.session['name'] = request.POST['name']
        if 'sex' in request.POST:
            request.session['sex'] = int(request.POST['sex'])
        if 'birthday' in request.POST:
            request.session['birthday'] = request.POST['birthday']
        if 'height' in request.POST:
            request.session['height'] = request.POST['height']
        if 'weight' in request.POST:
            request.session['weight'] = request.POST['weight']
        if 'activity' in request.POST:
            request.session['activity'] = request.POST['activity']

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

    if request.user.is_authenticated():
        physio = request.user.owner

    else:
        physio = {
            'name': request.session['name'] if 'name' in request.session else "",
            'sex': request.session.get('sex'),
            'birthday': request.session['birthday'] if 'birthday' in request.session else "",
            'height': request.session.get('height'),
            'weight': request.session.get('weight'),
            'activity': request.session.get('activity') if 'activity' in request.session else "",
        }

    return render(request, 'profiles/physiology.html', {
        'physio':   physio,
    })


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

    return render(request, 'profiles/regimes.html', {
        'health_regimes_list': health_regimes_list,
        'value_regimes_list': value_regimes_list
    })


def tastes(request):
    ingredient_list = []  # Ingredient.objects.all()  # TODO: Filter most frequent
    return render(request, 'profiles/tastes.html',
                  {'ingredients': [ingredient.name for ingredient in ingredient_list]})