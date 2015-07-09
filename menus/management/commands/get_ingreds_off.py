from django.core.management.base import BaseCommand
from menus.data.extract import get_food_array
from menus.models import IngredientFamily, Ingredient, IngredientNutriment, Nutriment


class Command(BaseCommand):
    """
    Fill database with ingredients/nutriments with the openfoodfacts.org data
    """
    help = ''

    def handle(self, *args, **options):
        import time
        start_time = time.time()

        print("Parsing csv...")

        csv = "menus/data/fr.openfoodfacts.org.products.csv"
        food_array = get_food_array(csv)

        print("Filling ingredients...")

        # Nutriments
        energy = Nutriment(name="energy_100g")
        energy.save()
        fat = Nutriment(name="fat_100g")
        fat.save()
        proteins = Nutriment(name="proteins_100g")
        proteins.save()
        carbohydrates = Nutriment(name="carbohydrates_100g")
        carbohydrates.save()

        n = 1
        for food in food_array:
            print(n, end='\r')
            n = n + 1
            # IngredientFamily
            category = food.main_category
            if not IngredientFamily.objects.filter(name=category):
                family = IngredientFamily(name=category)
                family.save()
            # Ingredient
            i = Ingredient()
            i.name = food.product_name
            i.family = IngredientFamily.objects.get(name=category)
            i.save()
            # Ingredient Nutriment relation
            ingredientToEnergy = IngredientNutriment(
                    ingredient = i,
                    nutriment=energy,
                    quantity = 0 if food.energy_100g == '' else food.energy_100g)
            ingredientToEnergy.save()
            ingredientToFat = IngredientNutriment(
                    ingredient = i,
                    nutriment=fat,
                    quantity = 0 if food.fat_100g == '' else food.fat_100g)
            ingredientToFat.save()
            ingredientToProteins = IngredientNutriment(
                    ingredient = i,
                    nutriment=proteins,
                    quantity = 0 if food.proteins_100g == '' else food.proteins_100g)
            ingredientToProteins.save()
            ingredientToCarbohydrates = IngredientNutriment(
                    ingredient = i,
                    nutriment=carbohydrates,
                    quantity = 0 if food.carbohydrates_100g == '' else food.carbohydrates_100g)
            ingredientToCarbohydrates.save()
        print()

        self.stdout.write('Done in %s seconds.' % (time.time() - start_time))