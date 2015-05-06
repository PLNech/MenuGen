__author__ = 'PLNech'

import random

from menus.models import Recipe

names_starter = [
    "Soupe miso",
    "Chips",
    "Soupe au chou",
    "Salade Océane",
    "Nachos",
    "Salade de chou",
    "Cornichons",
    "Fromage blanc",
    "Salade de champignons",
    "Tomate mozarella"
    ]

names_main = [
    "Poulet roti",
    "Pizza",
    "Chili",
    "Sushis",
    "Quesadilla",
    "Boeuf sauté",
    "Couscous",
    "Tajine",
    "crêpes jambon emmental",
    "Boeuf aux lentilles",
    "Boeuf boulgour",
    "Boeuf bourguignon",
    "Boeuf bourguignon",
    "Colin d'Alaska & Crevettes et riz sauce crudités",
    "Colin d'Alaska & légumes et riz sauce citron",
    "Colin d'alaska ail & fines herbes",
    "Collerettes Cuisson Rapide",
    "Galettes d'épeautre au son d'avoine",
    "Galettes de Céréales aux 2 Fromages Bio",
    "Galettes de Maïs",
    "Galettes de Maïs Bio",
    "Galettes de Maïs Bio extra-fines",
    "Galettes de Maïs au Chocolat Noir Bio",
    "Galettes de Normandie pur beurre",
    "Galettes de Pleyben",
    "Galettes de Riz",
    "Galettes de Riz Bio au Chocolat Noir",
    "Galettes de Riz Complet Bio",
    "Galettes de blé noir bio",
    "Macaroni",
    "Macaroni",
    "Macaroni & Cheese",
    ]

names_dessert = [
    "espresso",
    "fruitwater",
    "grand chocolat",
    "instant café",
    "la madeleine au beurre frais",
    "les crunchy",
    "marguerites",
    "pommes peches",
    "Gelato d'Italia Pesca Melba",
    "Gelato d'Italia Pistacchio",
    "Gelbe Orient Linsen",
    "Gelée Bonne Maman Coings",
    "Gelée Bonne Maman Framboises",
    "Gelée Bonne Maman Mûres",
    "Gelée Bonne Maman, Mûres",
    "Gelée Extra Groseilles",
    "Gelée au Madere",
    "Gelée au Madère",
    "Gelée de Marie Jeanne au piment d'Espelette",
    "Gelée de coing",
    "Gelée de mûres framboises",
    "Gelée extra Framboise",
    "Gelée extra de groseilles Leader Price",
    "Gelée extra goyave",
    "Gelée extra groseille",
    "Gelée extra maracudja",
    "Gelée framboise",
    "Gervais a boire",
    "Gervais maxi",
    "Gervais maxi",
    "Gervais maxi",
    "Gervais maxi framboise abricot",
    "Gervais à la vanille",
    "Gervais, fraise, abricot, framboise",
    "Gervita Nature",
    "Gervita Nature (10,3% MG)",
    "Macadamias",
    "Macaron aux framboises",
    "Macaron aux framboises",
    "Macaronade &quot;Fruits de mer&quot;",
    "Compote Pomme cuite au chaudron",
    "Compote Pomme-poire Bio Monoprix",
    "Compote Pommes Poires Carrefour",
    "Compote Pommes Vanille Carrefour",
    "Compote Pêches Bonne Maman",
    "Compote Pêches Brugnons avec morceaux fondants",
    "Compote Rhubarbe",
    "Compote allégée en sucres Pomme-Poire",
    "Compote allégée pomme banane",
    "Compote allégée pomme figue cannelle",
    "Compote allégée pomme fraise",
    "Compote allégée pomme poire",
    "Compote allégée pomme poire",
    "Compote allégée pomme poire",
    "Compote allégée pomme pêche",
    "Compote avec morceaux & pêche",
    "Compote de Pomme bio allégée en sucres",
    "Compote de Pommes Morceaux",
    "Compote de pomme",
    "Compote de pomme allégée en sucres Bio Monoprix",
    "Galettes bretonnes pur beurre",
    "Galettes bretonnes pur beurre",
    "Galettes bretonnes pur beurre pépites de chocolat Leader Price",
    "Galettes bretonnes pépites de chocolat",
    "Cake aux fruits",
    "Confiture allégée abricot",
    "Galettes chocolat Gayelord Hauser",
    ]

def generate_recipe(name):
    r = Recipe()
    r.name = name
    r.prep_time = random.randint(0, 30)
    r.cook_time = random.randint(0, 30)
    r.difficulty = random.randint(1, 3)
    r.price = random.randint(1, 3)
    return r


def generate_planning(nb_days, nb_meals_per_day):
    planning = []
    for j in range(nb_meals_per_day):
        daily_planning = []
        for i in range(nb_days):
            starter = generate_recipe(random.choice(names_starter))
            main = generate_recipe(random.choice(names_main))
            dessert = generate_recipe(random.choice(names_dessert))
            menu = {'starter': starter, 'main_course': main, 'dessert': dessert}
            daily_planning.append(menu)
        planning.append(daily_planning)

    return planning
