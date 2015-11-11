from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from menus.serializers import *
from django.contrib.auth.models import User


def landing(request):
    # request.session.flush()
    # if 'liked_aliments' not in request.session:
    # request.session['liked_aliments'] = ["Eau", "Chocolat", "Tagliatelles", "Dinde", "Poulet", "Boeuf", "Jambon", "Sucre", "Semoule", "Riz", "Spaghetti", "Lasagnes", "Framboise", "Fraise", "Cerise", "Groseille", "Pomme", "Poire", "Ananas", "Courgette", "Carotte", "Aubergine", "Tomate", "Radis", "Lait", "Oeuf", "Myrtille", "Farine", "Abricot", "Ail", "Oignon", "Saumon", "Beurre", "Fromage", "Fruits", "Légumes", "Viande", "Poisson", "Menthe", "Thym", "Huile de tournesol", "Basilique", "Petits pois", "Haricots verts" ]
    # if 'disliked_aliments' not in request.session:
    #     request.session['disliked_aliments'] = []

    return render(request, 'landing_s.html', {
        'landing': True})


def home(request):
    return render(request, 'menus/home.html', {})

@login_required
def statistics(request):
    family_freq = {}
    for i in Ingredient.objects.all():
        try:
            family_freq[i.family.name] = family_freq[i.family.name] + 1
        except KeyError:
            family_freq[i.family.name] = 1
    freq_family = {v:k for k, v in family_freq.items()}
    amount = sorted([k for k in freq_family.keys()])[-10:]
    families = [freq_family[k] for k in amount]

    pics = list()
    for r in Recipe.objects.all()[:200]:
        if r.picture:
            pics.append(r.picture)

    return render(request, 'menus/statistics.html', {
        'nb_recipes': Recipe.objects.all().count(),
        'nb_ingreds': Ingredient.objects.all().count(),
        'nb_nut': Nutriment.objects.all().count(),
        'nb_very_easy': Recipe.objects.filter(difficulty=0).count(),
        'nb_easy': Recipe.objects.filter(difficulty=1).count(),
        'nb_medium': Recipe.objects.filter(difficulty=2).count(),
        'nb_difficult': Recipe.objects.filter(difficulty=3).count(),
        'cat_amuse_gueule': Recipe.objects.filter(category='Amuse-gueule').count(),
        'cat_confiserie': Recipe.objects.filter(category='Confiserie').count(),
        'cat_conseil': Recipe.objects.filter(category='Conseil').count(),
        'cat_accompagnement': Recipe.objects.filter(category='Accompagnement').count(),
        'cat_dessert': Recipe.objects.filter(category='Dessert').count(),
        'cat_entree': Recipe.objects.filter(category='Entrée').count(),
        'cat_sauce': Recipe.objects.filter(category='Sauce').count(),
        'cat_boisson': Recipe.objects.filter(category='Boisson').count(),
        'cat_plat_principal': Recipe.objects.filter(category='Plat principal').count(),
        'families': families[:10],
        'amount': amount[:10],
        'pics': pics
    })

@login_required
def account(request):
    return render(request, 'profiles/account.html', {})

def call_to_action(request):
    return render(request, 'call_to_action_modal.html', {})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RecipeToIngredientViewSet(viewsets.ModelViewSet):
    queryset = RecipeToIngredient.objects.all()
    serializer_class = RecipeToIngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    # enable filter with query parameters such as /api/recipes?name=tarte
    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name:
            return Recipe.objects.filter(name__icontains=name)
        return Recipe.objects.all()
    serializer_class = RecipeSerializer


class DietViewSet(viewsets.ModelViewSet):
    queryset = Diet.objects.all()
    serializer_class = DietSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    # enable filter with query parameters such as /api/ingredients?name=sucre
    def get_queryset(self):
        name = self.request.query_params.get('name', None)
        if name:
            return Ingredient.objects.filter(name__icontains=name)
        return Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientNutrimentViewSet(viewsets.ModelViewSet):
    queryset = IngredientNutriment.objects.all()
    serializer_class = IngredientNutrimentSerializer


class IngredientFamilyViewSet(viewsets.ModelViewSet):
    queryset = IngredientFamily.objects.all()
    serializer_class = IngredientFamilySerializer


class NutrimentViewSet(viewsets.ModelViewSet):
    queryset = Nutriment.objects.all()
    serializer_class = NutrimentSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
