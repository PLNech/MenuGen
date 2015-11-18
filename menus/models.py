import datetime
import logging

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from stdimage.models import StdImageField

import menugen.defaults as default

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
    ('man', 'Homme'),
    ('woman', 'Femme'),
)

ACTIVITY = (
    ('low', 'Sédentaire'),
    ('light', 'Légère'),
    ('moderate', 'Modérée'),
    ('active', 'Régulière'),
    ('extreme', 'Intense'),
)

MEAL = (
    (0, 'midi'),
    (1, 'soir'),
)

logger = logging.getLogger("menus")


class Account(models.Model):
    user = models.OneToOneField(User)
    profile = models.OneToOneField('Profile')
    guests = models.ManyToManyField('Profile', related_name='guests')
    friends = models.ManyToManyField(User, related_name='friends')
    menus = models.ManyToManyField('Menu')


class Profile(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, default=default.NAME)
    birthday = models.DateField(blank=True, null=True, auto_now_add=True)
    weight = models.IntegerField(default=default.WEIGHT)
    height = models.FloatField(default=default.HEIGHT)
    sex = models.CharField(max_length=16, choices=SEX, default=default.SEX)
    activity = models.CharField(max_length=16, choices=ACTIVITY, blank=True, null=True, default=default.ACTIVITY)
    picture = StdImageField(upload_to='media/images/profiles', blank=True, null=True)

    unlikes_ingredient = models.ManyToManyField('Ingredient')
    unlikes_family = models.ManyToManyField('IngredientFamily')

    unlikes_recipe = models.ManyToManyField("Recipe")
    diets = models.ManyToManyField('Diet', related_name='diets')

    modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s: %d year-old %s of %dcm and %dkg, exercising %sly." \
               " Unlikes %d ingredients, %d families, and %d recipes. Follows %d diets." % (
                   str(self), self.age(), self.sex, self.height, self.weight, self.activity,
                   self.unlikes_ingredient.count(), self.unlikes_ingredient.count(), self.unlikes_ingredient.count(),
                   self.diets.count())

    def age(self):
        return relativedelta(datetime.date.today(), self.birthday).years

    def likes_dish(self, dish):
        try:
            recipe = Recipe.objects.get(name=dish.name)
        except Recipe.DoesNotExist:
            return True
        return self.likes_recipe(recipe)

    def likes_recipe(self, recipe):
        # If i dislike this dish, return false
        if self.unlikes_recipe.filter(name=recipe.name).exists():
            return False
        # If i dislike any ingredient, return false
        if recipe.ingredients.filter(bad_profiles__id=self.id).exists():
            return False

        # If i dislike any ingredient's family, return false
        if recipe.ingredients.filter(family__in=self.unlikes_family.all()).exists():
            return False
        return True


class RecipeToIngredient(models.Model):
    recipe = models.ForeignKey('Recipe')
    ingredient = models.ForeignKey('Ingredient')
    quantity = models.FloatField(blank=True, null=True, default=None)
    unit = models.CharField(max_length=128, blank=True, null=True, default=None)
    scraped_text = models.CharField(max_length=256, blank=True, null=True, default=None)
    parsed_name = models.CharField(max_length=256, blank=True, null=True, default=None)


class Recipe(models.Model):
    dom = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=128)
    picture = StdImageField(upload_to='media/images/recipe', blank=True, null=True)
    origin_url = models.URLField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    amount = models.IntegerField()
    difficulty = models.IntegerField(choices=EASE)
    price = models.IntegerField(choices=PRICE)
    steps = models.TextField(blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    drink = models.TextField(blank=True, null=True)

    ingredients = models.ManyToManyField('Ingredient', through=RecipeToIngredient)
    category = models.CharField(default="Plat", max_length=128)

    def __str__(self):
        return self.name

    @staticmethod
    def for_profile(profile, maximum=1000):
        """
        Returns up to maximum ingredients matching profile's criteria
        :type profile Profile
        :type maximum int
        :return:
        """
        count_recipes = Recipe.objects.count()

        if profile is None:
            recipes = Recipe.objects.order_by('?')
        else:
            # TODO: Use diets too
            logger.info('Excluding recipes for profile %d/%s from a corpus of %d recipes.' % (
                profile.id, profile.name, count_recipes))

            recipes = Recipe.objects.exclude(pk__in=profile.unlikes_recipe.values_list('pk'))
            logger.info('unlikes recipe : %d -> %d.' % (count_recipes, len(recipes)))
            count_recipes = len(recipes)

            recipes = recipes.exclude(ingredients__bad_profiles__pk=profile.pk)
            logger.info('unlikes ingredients : %d -> %d.' % (count_recipes, len(recipes)))  # FIXME: Does it work?
            count_recipes = len(recipes)

            recipes = recipes.exclude(ingredients__family__in=profile.unlikes_family.all())
            logger.info('unlikes families : %d -> %d.' % (count_recipes, len(recipes)))

            logger.info("Diets: reduced from %d to %d recipes." % (len(recipes), len(recipes)))
        return recipes[:maximum]


class Diet(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    picture = StdImageField(upload_to='media/images/diet', blank=True, null=True)

    ingredients = models.ManyToManyField('Ingredient')
    ingredients_family = models.ManyToManyField('IngredientFamily')
    active = False

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    # country =  #  FIXME : use it for local menu generation
    # season?
    family = models.ForeignKey('IngredientFamily')
    nutriments = models.ManyToManyField('Nutriment', through='IngredientNutriment')
    bad_diets = models.ManyToManyField('Diet')
    bad_profiles = models.ManyToManyField('Profile')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientNutriment(models.Model):
    ingredient = models.ForeignKey('Ingredient')
    nutriment = models.ForeignKey('Nutriment')
    quantity = models.FloatField()


class IngredientFamily(models.Model):
    name = models.CharField(max_length=64)
    ingredients = models.ManyToManyField('Ingredient')
    father = models.ForeignKey('IngredientFamily', null=True, default=None)
    bad_diets = models.ManyToManyField('Diet')

    def __str__(self):
        return self.name


class Nutriment(models.Model):
    name = models.CharField(max_length=128)
    unit_per_100g = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=32)
    price = models.IntegerField(choices=PRICE)
    difficulty = models.IntegerField(choices=EASE)
    nb_people = models.IntegerField()
    profiles = models.ManyToManyField('Profile')

    def __str__(self):
        return self.name


class Meal(models.Model):
    menu = models.ForeignKey('Menu')
    day = models.IntegerField()
    type = models.IntegerField(choices=MEAL)
    starter = models.ForeignKey('Recipe', related_name='starter')
    main_course = models.ForeignKey('Recipe', related_name='main_course')
    dessert = models.ForeignKey('Recipe', related_name='dessert')

# class Calendar(models.Model):
#
#     def __str__(self):
#         return self.name
