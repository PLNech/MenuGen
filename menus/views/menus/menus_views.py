from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from menus.forms import MenuForm
from menus.models import Menu

__author__ = 'kiyoakimenager'

@login_required
def menus(request):
    account = request.user.account
    user_menus = account.menus.all()
    menus_nb = user_menus.count()

    return render(request, 'menus/index.html', {
        'menus': user_menus,
        'menus_nb': menus_nb,

    })
    #
    # menus = []
    # menu_0 = Menu(name="Mon menu vacance")
    # menu_1 = Menu(name="Mon menu travail")
    # menus.append(menu_0)
    # menus.append(menu_1)
    # return render(request, 'menus/index.html', {'menus': menus})


@login_required
def new(request):
    if request.method == 'GET':
        form = MenuForm
        return render(request, 'menus/new_modal.html', {'form': form})
    else:
        form = MenuForm(data=request.POST)
        if form.is_valid():
            new_menu = form.menu_cache
            new_menu.nb_people = 1
            new_menu.price = 2
            new_menu.difficulty = 3
            new_menu.save()
            account = request.user.account
            account.menus.add(new_menu)
            return redirect('menus')

            """ for later use (AJAX) """
            # return render(request, 'profiles/guests/guest.html', {
            #     'menu': menu
            # })

        return HttpResponse(content=render(request, 'menus/new_modal.html', {'form': form}),
                            content_type='text/html; charset=utf-8',
                            status=form.error_code)
