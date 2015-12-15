# from rest_framework import serializers
#
# from menus.models import *
# from django.contrib.auth.models import User
#
#
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username', )
#
# class AccountSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('user', 'profile', 'guests', 'friends', 'menus')
#
# class ProfileSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('name', 'birthday', 'weight', 'height', 'sex', 'activity', 'picture',
#                   'unlikes', 'unlikes_family', 'unlikes_recipe', 'diets', 'modified')
#
# class RecipeToIngredientSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = RecipeToIngredient
#         fields = ('recipe', 'ingredient', 'quantity', 'unit', 'scraped_text', 'parsed_name')
#
# class RecipeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = ('dom', 'name', 'picture', 'origin_url', 'prep_time', 'cook_time', 'amount', 'difficulty',
#                   'price', 'steps', 'detail', 'drink', 'ingredients', 'category')
#
# class DietSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Diet
#         fields = ('name', 'description', 'picture', 'ingredients', 'ingredients_family')
#
# class IngredientSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Ingredient
#         fields = ('name', 'family', 'nutriments')
#
# class IngredientNutrimentSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = IngredientNutriment
#         fields = ('ingredient', 'nutriment', 'quantity')
#
# class IngredientFamilySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = IngredientFamily
#         fields = ('name', 'picture', 'ingredients', 'father')
#
# class NutrimentSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Nutriment
#         fields = ('name', 'unit_per_100g')
#
# class MenuSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Menu
#         fields = ('name', 'price', 'difficulty', 'nb_people', 'profiles')
#
# class MealSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Meal
#         fields = ('menu', 'day', 'type', 'starter', 'main_course', 'dessert')
