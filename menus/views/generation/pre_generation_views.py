import logging
from django.core import serializers
from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render
from menus.models import Profile
from menus.utils import json2obj

logger = logging.getLogger("menus")


def generate(request):
    """
        check nb_days and matrix existence
        if not :
            Set default nb days
            Set default menu's matrix into session
    """
    if 'nb_days' not in request.session:
        request.session['nb_days'] = 7
    if 'matrix' not in request.session:
        request.session['matrix'] = [[1 for _ in range(7)] for _ in range(2)]

    return render(request, 'menus/generate/generate.html',
                  {'days_range': range(0, request.session['nb_days']),
                   'nb_days': request.session['nb_days'],
                   'meals_matrix': request.session['matrix']})


def generate_select_profile(request):
    user = request.user
    guests = user.account.guests.all()
    logger.info("Guests: %r" % guests)
    guests = list(guests)
    logger.info("GuestList: %r" % guests)
    guests.append(user.account.profile)
    return render(request, 'menus/generate/select_profile.html', {'profiles': guests})


def generate_placements_detail(request):
    """
        Set nb_days according to input
        Set menu's matrix size based on nb_days and nb meal per day
        Set matrix content to true
    """

    nb_days = request.session.get('nb_days')
    if 'nb_days' in request.POST:
        nb_days = int(request.POST['nb_days'])
        if nb_days != request.session['nb_days']:
            request.session['nb_days'] = nb_days
            request.session['matrix'] = [[1 for x in range(nb_days)] for x in range(2)]

    return render(request, 'menus/generate/placements_detail.html',
                  {'days_range': range(0, nb_days),
                   'meals_matrix': request.session['matrix']})


def update_gen_criteria(request):
    """ This method is used as ajax call in order to update the pre-generation """
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])

    if 'budget' in request.POST:
        request.session['budget'] = request.POST.get('budget')
    if 'difficulty' in request.POST:
        request.session['difficulty'] = request.POST.get('difficulty')

    """ Set nb_days according to input
        Reset matrix content to true
    """
    if 'nb_days' in request.POST:
        nb_days = int(request.POST.get('nb_days'))
        request.session['nb_days'] = nb_days
        request.session['matrix'] = [[1 for x in range(nb_days)] for x in range(2)]

    """
        Update menu's matrice according to input
    """
    if 'matrix[day]' in request.POST:
        day = int(request.POST.get('matrix[day]'))
        meal = int(request.POST.get('matrix[meal]'))
        request.session['matrix'][meal][day] = int(request.POST.get('matrix[val]'))
        request.session.modified = True

    if 'lunch' in request.POST:
        is_checked = int(request.POST.get('lunch'))
        lunches = request.session['matrix'][0]
        print(lunches)
        request.session['matrix'][0] = [is_checked for x in lunches]
        request.session.modified = True

    if 'dinner' in request.POST:
        is_checked = int(request.POST.get('dinner'))
        dinners = request.session['matrix'][1]
        print(dinners)
        request.session['matrix'][1] = [is_checked for x in dinners]
        request.session.modified = True

    if 'profiles' in request.POST:
        profiles = request.POST.get('profiles')
        request.session['profiles'] = []
        profiles = json2obj(profiles)
        for profileData in profiles:
            try:
                profile = Profile.objects.filter(pk=profileData.id)
                profile_data = serializers.serialize("json", profile)
                if profileData.checked:
                    request.session['profiles'].append(profile_data)
                elif profile_data in request.session['profiles']:
                    request.session['profiles'].remove(profile_data)
            except Profile.DoesNotExist:
                pass
        logger.info("%d profiles loaded." % len(request.session['profiles']))

    # print(request.session.items())
    return HttpResponse('ok')
