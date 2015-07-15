from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def landing(request):
    # request.session.flush()
    # if 'liked_aliments' not in request.session:
    # request.session['liked_aliments'] = ["Eau", "Chocolat", "Tagliatelles", "Dinde", "Poulet", "Boeuf", "Jambon", "Sucre", "Semoule", "Riz", "Spaghetti", "Lasagnes", "Framboise", "Fraise", "Cerise", "Groseille", "Pomme", "Poire", "Ananas", "Courgette", "Carotte", "Aubergine", "Tomate", "Radis", "Lait", "Oeuf", "Myrtille", "Farine", "Abricot", "Ail", "Oignon", "Saumon", "Beurre", "Fromage", "Fruits", "Légumes", "Viande", "Poisson", "Menthe", "Thym", "Huile de tournesol", "Basilique", "Petits pois", "Haricots verts" ]
    # if 'disliked_aliments' not in request.session:
    #     request.session['disliked_aliments'] = []

    return render(request, 'landing.html', {
        'landing': True})


def home(request):
    return render(request, 'menus/home.html', {})

@login_required
def statistics(request):
    return render(request, 'menus/statistics.html', {})

@login_required
def account(request):
    return render(request, 'profiles/account.html', {})

