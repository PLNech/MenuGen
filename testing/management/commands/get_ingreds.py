from django.core.management.base import BaseCommand
from testing.models import Ingredient, Nutriment
import time

class Command(BaseCommand):
    """
    Fill database with ingredients from the Ciqual ANSES table
    """
    help = ''

    def handle(self, *args, **options):
        csv = "testing/CIQUAL2013-Donneescsv.csv"
        print("Parsing %s and filling the database..." % csv)
        start_time = time.time()

        separator = ";"
        with open(csv, 'r', encoding="ISO-8859-1") as f:

            # Nutriments
            fields = f.readline().rstrip("\n").split(separator)
            for i in range(4, 60):
                name = fields[i] if fields[i] and fields[i] != "-" else None
                if name:
                    name = name.split(" ")[1:-1] # remove leading number and trailing unit
                    nutriment = Nutriment(name=name)
                    nutriment.save()

            for n, line in enumerate(f.readlines()):
                print("%s ingredients processed" % n, end='\r')
                fields = line.rstrip("\n").split(separator)

                # Ingredients
                name = fields[3] if fields[3] and fields[3] != "-" else None
                category = fields[1] if fields[1] and fields[1] != "-" else None
                ingredient = Ingredient(name=name, category=category)
                ingredient.save()

        print('Done in %s seconds.' % (time.time() - start_time))
