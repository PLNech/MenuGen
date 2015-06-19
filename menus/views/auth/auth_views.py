from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

__author__ = 'kiyoakimenager'

from menus.forms import RegistrationForm, SignInForm

def sign_in(request):
    if request.method == "GET":
        form = SignInForm
        return render(request, 'auth/sign_in.html', {'form': form})
    if request.method == "POST":
        form = SignInForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect('menus.views.friends')
        return HttpResponse(content=render(request, 'auth/sign_in.html', {'form': form}),
                            content_type='text/html; charset=utf-8',
                            status=form.error_code)

def sign_up(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'auth/sign_up.html', {'form': form})
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.user_cache
            user = authenticate(username=user.username, password=request.POST['password1'])
            login(request, user)

            return redirect('menus.views.friends')
        return HttpResponse(content=render(request, 'auth/sign_up.html', {'form': form}),
                                content_type='text/html; charset=utf-8',
                                status=400)

@login_required
def sign_out(request):
    logout(request)
    return redirect('menus.views.landing')