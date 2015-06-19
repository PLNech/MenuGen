#! /usr/bin/env python
from codecs import open
from collections import defaultdict


class CsvFood(object):
    empty_values = [None, '', ' ']

    fields_all = {
        'code': 0,
        'product_name': 7,
        'generic_name': 8,
        'quantity': 9,
        'categories': 14,
        'categories_tags': 15,
        'origins': 17,
        'origins_tags': 18,
        'manufacturing_places': 19,
        'ingredients_text': 34,
        'allergens': 35,
        'traces': 37,
        'traces_tags': 38,
        'serving_size': 39,
        'ingredients_from_palm_oil': 46,
        'ingredients_from_palm_oil_tags': 47,
        'main_category': 58,
        'image_url': 60,
        'image_small_url': 61,
        'energy_100g': 62,
        'fat_100g': 63,
        'saturated_fat_100g': 64,
        'butyric_acid_100g': 65,
        'caproic_acid_100g': 66,
        'caprylic_acid_100g': 67,
        'capric_acid_100g': 68,
        'lauric_acid_100g': 69,
        'myristic_acid_100g': 70,
        'palmitic_acid_100g': 71,
        'stearic_acid_100g': 72,
        'arachidic_acid_100g': 73,
        'behenic_acid_100g': 74,
        'lignoceric_acid_100g': 75,
        'cerotic_acid_100g': 76,
        'montanic_acid_100g': 77,
        'melissic_acid_100g': 78,
        'monounsaturated_fat_100g': 79,
        'polyunsaturated_fat_100g': 80,
        'omega_3_fat_100g': 81,
        'alpha_linolenic_acid_100g': 82,
        'eicosapentaenoic_acid_100g': 83,
        'docosahexaenoic_acid_100g': 84,
        'omega_6_fat_100g': 85,
        'linoleic_acid_100g': 86,
        'arachidonic_acid_100g': 87,
        'gamma_linolenic_acid_100g': 88,
        'dihomo_gamma_linolenic_acid_100g': 89,
        'omega_9_fat_100g': 90,
        'oleic_acid_100g': 91,
        'elaidic_acid_100g': 92,
        'gondoic_acid_100g': 93,
        'mead_acid_100g': 94,
        'erucic_acid_100g': 95,
        'nervonic_acid_100g': 96,
        'trans_fat_100g': 97,
        'cholesterol_100g': 98,
        'carbohydrates_100g': 99,
        'sugars_100g': 100,
        'sucrose_100g': 101,
        'glucose_100g': 102,
        'fructose_100g': 103,
        'lactose_100g': 104,
        'maltose_100g': 105,
        'maltodextrins_100g': 106,
        'starch_100g': 107,
        'polyols_100g': 108,
        'fiber_100g': 109,
        'proteins_100g': 110,
        'casein_100g': 111,
        'serum_proteins_100g': 112,
        'nucleotides_100g': 113,
        'salt_100g': 114,
        'sodium_100g': 115,
        'alcohol_100g': 116,
        'vitamin_a_100g': 117,
        'vitamin_d_100g': 118,
        'vitamin_e_100g': 119,
        'vitamin_k_100g': 120,
        'vitamin_c_100g': 121,
        'vitamin_b1_100g': 122,
        'vitamin_b2_100g': 123,
        'vitamin_pp_100g': 124,
        'vitamin_b6_100g': 125,
        'vitamin_b9_100g': 126,
        'vitamin_b12_100g': 127,
        'biotin_100g': 128,
        'pantothenic_acid_100g': 129,
        'silica_100g': 130,
        'bicarbonate_100g': 131,
        'potassium_100g': 132,
        'chloride_100g': 133,
        'calcium_100g': 134,
        'phosphorus_100g': 135,
        'iron_100g': 136,
        'magnesium_100g': 137,
        'zinc_100g': 138,
        'copper_100g': 139,
        'manganese_100g': 140,
        'fluoride_100g': 141,
        'selenium_100g': 142,
        'chromium_100g': 143,
        'molybdenum_100g': 144,
        'iodine_100g': 145,
        'caffeine_100g': 146,
        'taurine_100g': 147,
        'ph_100g': 148,
        'fruits_vegetables_nuts_100g': 149,
        'collagen_meat_protein_ratio_100g': 150,
        'carbon_footprint_100g': 151
    }
    # Fields needed for further data manipulation
    fields_needed = [
        'product_name',
        'quantity',
        # 'categories',
        'energy_100g',
        'fat_100g',
        'proteins_100g',
        'carbohydrates_100g',
        'image_url',
        'image_small_url'
    ]

    # Fields where more than 70% of data was empty
    fields_useless = ['origins',
                      'origins_tags',
                      'manufacturing_places',
                      'traces',
                      'traces_tags',
                      'allergens',
                      'alcohol_100g',
                      'calcium_100g',
                      'ingredients_from_palm_oil_tags',
                      'polyunsaturated_fat_100g',
                      'monounsaturated_fat_100g',
                      'iron_100g',
                      'vitamin_c_100g',
                      'cholesterol_100g',
                      'vitamin_b1_100g',
                      'magnesium_100g',
                      'vitamin_a_100g',
                      'vitamin_e_100g',
                      'vitamin_b6_100g',
                      'vitamin_b9_100g',
                      'vitamin_pp_100g',
                      'vitamin_b2_100g',
                      'trans_fat_100g',
                      'phosphorus_100g',
                      'vitamin_b12_100g',
                      'vitamin_d_100g',
                      'omega_3_fat_100g',
                      'potassium_100g',
                      'pantothenic_acid_100g',
                      'starch_100g',
                      'carbon_footprint_100g',
                      'polyols_100g',
                      'biotin_100g',
                      'zinc_100g',
                      'omega_6_fat_100g',
                      'lactose_100g',
                      'alpha_linolenic_acid_100g',
                      'chloride_100g',
                      'iodine_100g',
                      'linoleic_acid_100g',
                      'bicarbonate_100g',
                      'fluoride_100g',
                      'manganese_100g',
                      'copper_100g',
                      'selenium_100g',
                      'docosahexaenoic_acid_100g',
                      'fruits_vegetables_nuts_100g',
                      'vitamin_k_100g',
                      'collagen_meat_protein_ratio_100g',
                      'silica_100g',
                      'caffeine_100g',
                      'eicosapentaenoic_acid_100g',
                      'fructose_100g',
                      'taurine_100g',
                      'casein_100g',
                      'ph_100g',
                      'omega_9_fat_100g',
                      'maltodextrins_100g',
                      'sucrose_100g',
                      'serum_proteins_100g',
                      'arachidonic_acid_100g',
                      'chromium_100g',
                      'glucose_100g',
                      'nucleotides_100g',
                      'oleic_acid_100g',
                      'arachidic_acid_100g',
                      'lauric_acid_100g',
                      'molybdenum_100g', 'behenic_acid_100g',
                      'butyric_acid_100g',
                      'capric_acid_100g',
                      'caproic_acid_100g',
                      'caprylic_acid_100g',
                      'cerotic_acid_100g',
                      'dihomo_gamma_linolenic_acid_100g',
                      'elaidic_acid_100g',
                      'erucic_acid_100g',
                      'gamma_linolenic_acid_100g',
                      'gondoic_acid_100g',
                      'ingredients_from_palm_oil',
                      'lignoceric_acid_100g',
                      'maltose_100g',
                      'mead_acid_100g',
                      'melissic_acid_100g',
                      'montanic_acid_100g',
                      'myristic_acid_100g',
                      'nervonic_acid_100g',
                      'palmitic_acid_100g',
                      'stearic_acid_100g']

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def __init__(self, fields):
        product_name_index = CsvFood.fields_all['product_name']
        generic_name_index = CsvFood.fields_all['generic_name']

        if fields[product_name_index] not in CsvFood.empty_values:
            self.product_name = fields[product_name_index]
        elif fields[generic_name_index] not in CsvFood.empty_values:
            self.product_name = fields[generic_name_index]

        for (name, index) in CsvFood.fields_all.items():
            if name in CsvFood.fields_useless:
                continue
            setattr(self, name, fields[index])

    def print(self):
        pass


def print_fields(fields):
    print(fields[7])
    print(fields[9])
    print(fields[17])
    print(fields[18])
    print(fields[19])
    print(fields[20])
    print(fields[34])
    print(fields[35])
    print(fields[37])
    print(fields[38])
    print(fields[39])
    print(fields[42])
    print(fields[43])
    print(fields[46])
    print(fields[47])
    print(fields[58])
    print(fields[60])
    print(fields[61])
    for i in range(62, 152):
        print(fields[i])


def quick_print(attribute, s):
    if attribute != '':
        print(s + ": " + attribute)


def print_stats(food_array):
    stats = defaultdict(int)
    list_fields = []
    item_count = len(food_array)

    for item in food_array:
        item_dict = dict(item)
        for key, value in item_dict.items():
            if value in [None, '', ' ']:
                stats[key] += 1
                assert (len(value) < 2)

    for key, value in stats.items():
        stats[key] = value

    for key in sorted(stats):
        value = 100 * stats[key] / item_count
        list_fields.append((key, value))

    for pair in sorted(list_fields, key=lambda x: x[1]):
        print("%s was null %.2f%% times." % (pair[0], pair[1]))

    print("\nFinished analysing %d items." % item_count)


def is_invalid_field_list(fields):
    """
    Returns true if the given line is not a valid field list

    :param fields: Fields of the line to test
    :type fields list
    :rtype bool
    """
    return len(fields) != 154


def has_no_name(fields):
    """
    Returns true if the product has no usable name

    :param fields: Fields of the line to test
    :type fields list
    :rtype bool
    """
    product_name_index = CsvFood.fields_all['product_name']
    generic_name_index = CsvFood.fields_all['generic_name']

    return fields[product_name_index] in CsvFood.empty_values \
        and fields[generic_name_index] in CsvFood.empty_values


def invalid_fields(item):
    """
    Returns the needed fields that are missing from this product

    :param item: The product to test
    :type item CsvFood
    :return The list of missing fields (if any)
    :rtype list
    """
    invalids = []
    for field in CsvFood.fields_needed:
        if not hasattr(item, field):
            print("item had no %s." % field)
            invalids.append(field)

        value = getattr(item, field, -42)
        if value in [-42, '']:
            invalids.append(field)
    return invalids

def get_food_array(csv):
    separator = "\t"
    i = 0
    with open(csv, 'r', 'utf-8') as f:
        food_array = []
        fields = f.readline()
        for i, line in enumerate(f):
            fields = line.rstrip("\n").split(separator)
            if is_invalid_field_list(fields) or has_no_name(fields):
                continue
            food = CsvFood(fields)
            if invalid_fields(food):
                continue
            food_array.append(food)
        return food_array


if __name__ == '__main__':
    skip_count_lines = 0
    skip_count_items = 0
    skip_count_fields = defaultdict(int)
    csv = "fr.openfoodfacts.org.products.csv"
    separator = "\t"
    i = 0
    with open(csv, 'r', 'utf-8') as f:
        # fields = f.readline().split(separator)
        food_array = []
        # remove field names
        fields = f.readline()
        filled = 0
        for i, line in enumerate(f):
            fields = line.rstrip("\n").split(separator)
            loc_filled = len([x for x in fields if x is not ' ' and x is not '' and x is not None])
            filled += loc_filled
            if is_invalid_field_list(fields) or has_no_name(fields):
                skip_count_lines += 1
                continue
            food = CsvFood(fields)
            useless_fields = invalid_fields(food)
            if useless_fields:
                for useless_f in useless_fields:
                    skip_count_fields[useless_f] += 1
                skip_count_items += 1
                continue
            food_array.append(food)
        filled /= i
        print("Loaded %d lines." % i)
        print("Items had on average %d fields filled." % filled)
        print("Skipped %d lines with encoding errors." % skip_count_lines)
        print("Skipped %d items missing needed attribute(s)." % skip_count_items)
        for field, skip_count in sorted(skip_count_fields.items(), key=lambda x: x[1]):
            print("-\t%d items had no %s." % (skip_count, field))
        print_stats(food_array)
