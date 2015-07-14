import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from stdimage.models import StdImageField

EASE = (
    (0, 'Très facile'),
    (1, 'Facile'),
    (2, 'Moyenne'),
    (3, 'Difficile'),
)

PRICE = (
    (0, 'Bon marché'),
    (1, 'Moyen'),
    (2, 'Assez cher'),
)

SEX = (
    (0, 'Homme'),
    (1, 'Femme'),
)

ACTIVITY = (
    (0, 'Jamais'),
    (1, 'De temps en temps'),
    (2, 'Souvent'),
    (3, 'Tout le temps'),
)


class Account(models.Model):
    user = models.OneToOneField(User)
    profile = models.OneToOneField('Profile')
    guests = models.ManyToManyField('Profile', related_name='guests')
    friends = models.ManyToManyField(User, related_name='friends')
    menus = models.ManyToManyField('Menu')


class Profile(models.Model):
    name = models.CharField(max_length=64, default='Sans nom')
    birthday = models.DateField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    sex = models.IntegerField(choices=SEX, blank=True, null=True)
    activity = models.IntegerField(choices=ACTIVITY, blank=True, null=True)
    picture = StdImageField(upload_to='media/images/profiles')

    unlikes = models.ManyToManyField('Ingredient')
    unlikes_family = models.ManyToManyField('IngredientFamily')
    diets = models.ManyToManyField('Diet')

    modified = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name


class RecipeToIngredient(models.Model):
    recipe = models.ForeignKey('Recipe')
    ingredient = models.ForeignKey('Ingredient')
    quantity = models.FloatField(blank=True, null=True, default=None)
    unit = models.CharField(max_length=128, blank=True, null=True, default=None)


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    picture = StdImageField(upload_to='media/images/recipe')
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    amount = models.IntegerField()
    difficulty = models.IntegerField(choices=EASE)
    price = models.IntegerField(choices=PRICE)
    steps = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    drink = models.TextField(blank=True, null=True)
    origin_url = models.URLField()

    ingredients = models.ManyToManyField('Ingredient', through=RecipeToIngredient)
    category = models.CharField(default="Plat", max_length=128)

    def __str__(self):
        return self.name


class Diet(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    picture = StdImageField(upload_to='media/images/diet')

    ingredients = models.ManyToManyField('Ingredient')
    ingredients_family = models.ManyToManyField('IngredientFamily')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    # country =  #  FIXME : use it for local menu generation
    # season?
    family = models.ForeignKey('IngredientFamily')
    nutriments = models.ManyToManyField('Nutriment', through='IngredientNutriment')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientNutriment(models.Model):
    ingredient = models.ForeignKey('Ingredient')
    nutriment = models.ForeignKey('Nutriment')
    quantity = models.FloatField()


class IngredientFamily(models.Model):
    name = models.CharField(max_length=32)
    picture = StdImageField(upload_to='media/images/ingredient_family')

    ingredients = models.ManyToManyField('Ingredient')

    # TODO (addition by Kevin) : seems necessary for hierarchy (to discuss)
    father = models.ForeignKey('IngredientFamily', null=True, default=None)

    def __str__(self):
        return self.name


class Nutriment(models.Model):
    name = models.CharField(max_length=128)
    unit_per_100g = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=32)
    people_n = models.IntegerField()
    price = models.IntegerField(choices=PRICE)
    difficulty = models.IntegerField(choices=EASE)
    # FIXME : missing order/planning relationship (will do it soon) - kevin
    recipes = models.ManyToManyField('Recipe')

    def __str__(self):
        return self.name
