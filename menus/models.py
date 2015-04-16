from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    SEX = (
        (0, 'male'),
        (1, 'female'),
    )

    #user = models.ForeignKey('User')
    name = models.CharField(max_length=64)
    birthday = models.DateField()
    weight = models.IntegerField()
    height = models.IntegerField()
    sex = models.IntegerField(choices=SEX)
    activity = models.IntegerField()  # FIXME : quantification? jamais, occasionellemen, régiulierement, intrensiveme,t
    #picture = models.ImageField()


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    #picture = models.ImageField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    amount = models.IntegerField()
    difficulty = models.IntegerField()  # FIXME : quantification? facile, moyen difficile
    price = models.IntegerField()  # FIXME : quantification? check marmitton
    #category = models.CharField()  # TODO : relation
    steps = models.TextField()
    detail = models.TextField()
    drink = models.TextField()
    origin_url = models.URLField()


class Diet(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    #picture = models.ImageField()


class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    #picture = models.ImageField()
    description = models.TextField()
    # country =  #  FIXME : use it for local menu generation
    # season?
    family = models.ForeignKey('IngredientFamily')


class IngredientFamily(models.Model):
    name = models.CharField(max_length=32)
    #picture = models.ImageField()


class Nutriment(models.Model):
    name = models.CharField(max_length=32)


class Menu(models.Model):
    name = models.CharField(max_length=32)
    people_n = models.IntegerField()
    price = models.IntegerField()  # FIXME : marmitton
    difficulty = models.IntegerField()  # FIXME : marmitton

