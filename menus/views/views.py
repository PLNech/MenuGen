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
    return render(request, 'menus/statistics.html', {})

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
