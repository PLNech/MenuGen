from django.shortcuts import render


def home(request):
    return render(request, 'menus/home.html', {})


def generate(request):
    return render(request, 'menus/generate.html', {})


def menus(request):
    return render(request, 'menus/menus.html', {})


def friends(request):
    return render(request, 'menus/friends.html', {})


def statistics(request):
    return render(request, 'menus/statistics.html', {})


def preferences(request):
    return render(request, 'profile/preferences.html', {})


def regimes(request):
    return render(request, 'profile/regimes.html', {})


def tastes(request):
    return render(request, 'profile/tastes.html', {})


def account(request):
    return render(request, 'profile/account.html', {})


def sign_in(request):
    return render(request, 'auth/sign_in.html', {})


def sign_up(request):
    return render(request, 'auth/sign_up.html', {})


def sign_out(request):
    return render(request, 'auth/sign_out.html', {})