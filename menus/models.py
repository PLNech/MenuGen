import datetime
import logging
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.utils import timezone
from djutils.decorators import async
from stdimage.models import StdImageField
import menugen.defaults as default
from menus.utils import list_pk

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

    def my_key_recipe_criteria(self):
        return "d:%s|f:%s|r:%s|i:%s" % (list_pk(self.diets),
                                        list_pk(self.unlikes_family),
                                        list_pk(self.unlikes_recipe),
                                        list_pk(self.unlikes_ingredient))

    @staticmethod
    def key_recipe_criteria(profiles):
        diets = None
        families = None
        recipes = None
        ings = None
        logger.info("Creating key for %d profiles." % len(profiles))

        for profile in profiles:
            p_diets = profile.diets.all()
            p_family = profile.unlikes_family.all()
            p_recipe = profile.unlikes_recipe.all()
            p_ings = profile.unlikes_ingredient.all()
            diets = diets | p_diets if diets else p_diets
            families = families | p_family if families else p_family
            recipes = recipes | p_recipe if recipes else p_recipe
            ings = ings | p_ings if ings else p_ings

        return "d:%s|f:%s|r:%s|i:%s" % (list_pk(diets),
                                        list_pk(families),
                                        list_pk(recipes),
                                        list_pk(ings))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s: %d year-old %s of %dcm and %dkg, exercising %sly." \
               " Unlikes %d ingredients, %d families, and %d recipes. Follows %d diets." % (
                   str(self), self.age(), self.sex, self.height, self.weight, self.activity,
                   0 if self._state.adding else self.unlikes_ingredient.count(),
                   0 if self._state.adding else self.unlikes_family.count(),
                   0 if self._state.adding else self.unlikes_recipe.count(),
                   0 if self._state.adding else self.diets.count())

    def age(self):
        return relativedelta(datetime.date.today(), self.birthday).years

    def likes_dish(self, dish):
        try:
            recipe = Recipe.objects.filter(name=dish.name).first()
        except Recipe.DoesNotExist:
            return True
        return self.likes_recipe(recipe)

    def likes_recipe(self, recipe):
        # if i am not a real profile, return true
        if self._state.adding:
            return True
        # If i dislike this dish, return false
        if self.unlikes_recipe.filter(name=recipe.name).exists():
            return False
        # If i dislike any ingredient, return false
        if recipe.ingredients.filter(bad_profiles__id=self.pk).exists():
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
    def for_profile_async(profile, maximum=1000):
        return Recipe.for_profiles_async([profile, ], maximum)

    @staticmethod
    @async
    def for_profiles_async(profiles_list, maximum=1000):
        logger.info("Beginning asynchronous recipe list generation.")
        Recipe.for_profiles(profiles_list, maximum)
        logger.info("Finished asynchronous recipe list generation.")

    @staticmethod
    def for_profiles(profile_list, maximum=1000):
        """
        Returns up to maximum ingredients matching profile's criteria
        :type profile_list list
        :type maximum int
        :return:
        """
        if profile_list is None:
            recipes = Recipe.objects.order_by('?')
        else:
            profile_list.sort(key=lambda p: p.name)
            key_profiles_criteria = "recipes_" + Profile.key_recipe_criteria(profile_list)

            # Cache lookup to avoid recalculation of recipe criteria
            recipes = cache.get(key_profiles_criteria)
            if recipes is not None:
                logger.info(
                    "Found recipe list (%d recipes) in cache for key \"%s\"." % (len(recipes), key_profiles_criteria))
                return recipes[:maximum]

            logger.info("Calculating profiles for key \"%s\"." % key_profiles_criteria)

            count_recipes = Recipe.objects.count()
            count_recipes_first = count_recipes
            profile_diets_pks = [profile.diets.values_list('pk') for profile in profile_list]
            profile_bad_recipes_pks = [profile.unlikes_recipe.values_list('pk') for profile in profile_list]
            profile_bad_families_pks = [profile.unlikes_family.values_list('pk') for profile in profile_list]
            profile_bad_ings_pks = [profile.unlikes_ingredient.values_list('pk') for profile in profile_list]

            # Flattening lists and de-tupling items
            profile_diets = list(set([item[0] for sublist in profile_diets_pks for item in sublist]))
            profile_bad_ings = list(set([item[0] for sublist in profile_bad_ings_pks for item in sublist]))
            profile_bad_families = list(set([item[0] for sublist in profile_bad_families_pks for item in sublist]))
            profile_bad_recipes = list(set([item[0] for sublist in profile_bad_recipes_pks for item in sublist]))

            recipes = Recipe.objects
            count_recipes = recipes.count()

            logger.info('Excluding recipes for profiles %s from a corpus of %d recipes.' % (
                ", ".join([str(profile.id) + ": " + profile.name for profile in profile_list]), count_recipes))

            # Diet Families
            recipes = recipes.exclude(ingredients__family__bad_diets__pk__in=profile_diets)
            count_recipes_new = len(recipes)
            logger.info('unlikes diet families : %d -> %d.' % (count_recipes, count_recipes_new))
            count_recipes = count_recipes_new

            # Diet Ingredients
            recipes = recipes.exclude(ingredients__bad_diets__pk__in=profile_diets)
            count_recipes_new = len(recipes)
            logger.info('unlikes diet ingredients : %d -> %d.' % (count_recipes, count_recipes_new))
            count_recipes = count_recipes_new

            # Profiles families
            recipes = recipes.exclude(ingredients__family__pk__in=profile_bad_families)
            count_recipes_new = len(recipes)
            logger.info('unlikes families : %d -> %d.' % (count_recipes, count_recipes_new))
            count_recipes = len(recipes)

            # Profiles recipes
            recipes = recipes.exclude(pk__in=profile_bad_recipes)
            count_recipes_new = len(recipes)
            logger.info('unlikes recipe : %d -> %d.' % (count_recipes, count_recipes_new))
            count_recipes = len(recipes)

            # Profiles ingredients
            recipes = recipes.exclude(ingredients__pk__in=profile_bad_ings)
            count_recipes_new = len(recipes)
            logger.info('unlikes ingredients : %d -> %d.' % (count_recipes, count_recipes_new))  # FIXME: Does it work?

            logger.info("for_profile: reduced from %d to %d recipes." % (count_recipes_first, count_recipes_new))

            cache.set(key_profiles_criteria, recipes, None)
            logger.info("Updated cache value for %s." % key_profiles_criteria)
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
