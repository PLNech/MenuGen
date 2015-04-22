from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def landing(request):
    return render(request, 'landing.html', {})


def home(request):
    return render(request, 'menus/home.html', {})


def generate(request):
    return render(request, 'menus/generate/generate.html', {'days': range(0, 7)})


def generate_select_profile(request):
    return render(request, 'menus/generate/select_profile.html', {})


def generate_placements_detail(request):
    return render(request, 'menus/generate/placements_detail.html', {'days': range(0, 7)})


def generation(request):
    return render(request, 'menus/generation.html', {'days': range(0, 7)})


@login_required
def menus(request):
    return render(request, 'menus/menus.html', {})


@login_required
def friends(request):
    return render(request, 'menus/friends.html', {})


@login_required
def statistics(request):
    return render(request, 'menus/statistics.html', {})


def physiology(request):
    if request.method == 'POST':
        username = request.POST['username']
        sex = request.POST['sex']
        height = request.POST['height']
        weight = request.POST['weight']
    else:
        return render(request, 'profile/physiology.html', {'ages': range(6, 150)})


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
                return redirect('menus.views.sign_in')
        else:
            return redirect('menus.views.sign_in')
    else:
        return render(request, 'auth/sign_in.html', {})


def sign_up(request):
    return render(request, 'auth/sign_up.html', {})


@login_required
def sign_out(request):
    logout(request)
    return redirect('menus.views.landing')