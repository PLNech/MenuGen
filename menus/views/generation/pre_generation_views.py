from django.http import HttpResponseNotAllowed, HttpResponse
from django.shortcuts import render

__author__ = 'kiyoakimenager'

def generate(request):
    return render(request, 'menus/generate/generate.html',
                  {'days_range': range(0, 7)})


def generate_select_profile(request):
    return render(request, 'menus/generate/select_profile.html', {})


def generate_placements_detail(request):
    nb_days = int(request.POST['nb_days'])
    return render(request, 'menus/generate/placements_detail.html',
                  {'days_range': range(0, nb_days)})

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
