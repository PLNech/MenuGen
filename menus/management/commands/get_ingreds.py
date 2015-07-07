from django.core.management.base import BaseCommand
from menus.models import Ingredient, IngredientFamily, IngredientNutriment, Nutriment
import time

class Command(BaseCommand):
    """
    Fill database with ingredients/nutriments from the Ciqual ANSES table
    """
    help = ''

    def handle(self, *args, **options):
        csv = "testing/CIQUAL2013-Donneescsv.csv"
        print("Parsing %s and filling the database..." % csv)
        start_time = time.time()

        separator = ";"
        with open(csv, 'r', encoding="ISO-8859-1") as f:

            # Nutriments
            nutriments = []
            fields = f.readline().rstrip("\n").split(separator)
            for i in range(4, 60):
                name = fields[i]
                unit_per_100g = name.split(" ")[2][1:-6]
                name = name.split(" ")[1:-1][0]
                nutriment = Nutriment(name=name, unit_per_100g=unit_per_100g)
                nutriment.save()
                nutriments.append(nutriment)

            for n, line in enumerate(f.readlines()):
                print("%s ingredients processed" % n, end='\r')
                fields = line.rstrip("\n").split(separator)

                # Ingredients
                name = fields[3] if fields[3] and fields[3] != "-" else None
                category = fields[1] if fields[1] and fields[1] != "-" else None
                try:
                    family = IngredientFamily.objects.filter(name=category)[0]
                except IndexError:
                    family = IngredientFamily(name=category)
                    family.save()
                ingredient = Ingredient(name=name, family=family)
                ingredient.save()

                # Ingredient Nutriment relations
                for i in range(4, 60):
                    quantity = fields[i] if fields[i] and fields[i] != "-" else "0"
                    quantity = quantity.replace("< ", "")
                    quantity = quantity.replace("traces", "0.01")
                    quantity = float(quantity.replace(",", "."))
                    ingredToNut = IngredientNutriment(
                        ingredient=ingredient,
                        nutriment=nutriments[i - 4],
                        quantity=quantity
                    )
                    ingredToNut.save()

        print('Done in %s seconds.' % (time.time() - start_time))
