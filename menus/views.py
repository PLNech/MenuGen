from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def landing(request):
    return render(request, 'landing.html', {})


@login_required
def home(request):
    return render(request, 'menus/home.html', {})


@login_required
def generate(request):
    return render(request, 'menus/generate.html', {})


@login_required
def menus(request):
    return render(request, 'menus/menus.html', {})


@login_required
def friends(request):
    return render(request, 'menus/friends.html', {})


@login_required
def statistics(request):
    return render(request, 'menus/statistics.html', {})


@login_required
def preferences(request):
    return render(request, 'profile/preferences.html', {})


@login_required
def regimes(request):
    return render(request, 'profile/regimes.html', {})


@login_required
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
                return redirect('menus.views.home')
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