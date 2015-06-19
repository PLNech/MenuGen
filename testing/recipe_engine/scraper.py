#! /usr/bin/env python
# coding: utf-8

import requests
import os
import random
from testing.recipe_engine.parser import Ingredient
from bs4 import BeautifulSoup
from subprocess import call


class Recipe:
    """ Scrap recipe from a marmiton url """

    def sanitize(self, s):
        """
        remove extra whitespaces, leading and trailing whitespaces, extra spaces
        """
        if s:
            s = s.replace("\r", "")
            s = s.replace("\n", "")
            s = s.replace("\t", "")
            while (len(s) > 0 and s[0] == " "):
                s = s[1:]
            while (len(s) > 0 and s.endswith(" ")):
                s = s[:-1]
            while (s != s.replace("  ", " ")):
                s = s.replace("  ", " ")
            return s
        else:
            return None;

    def __init__(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text)

        self.title = soup.find("span", "fn").string if soup.find("span", "fn") else None
        self.url = response.url
        self.picture_url = soup.find("img", { "class" : "photo"})['src'] if soup.find("img", { "class" : "photo"}) else None

        txt = soup.find("div", { "class" : "m_content_recette_breadcrumb"}).string if soup.find("div", { "class" : "m_content_recette_breadcrumb"}) else None
        if txt and not " - " in txt:
            txt = None
        self.meal_type = txt.split(" - ")[0] if txt else None
        self.difficulty = txt.split(" - ")[1] if txt else None
        self.price_range = txt.split(" - ")[2] if txt else None

        self.preptime = soup.find("span", { "class" : "preptime" }).text if soup.find("span", { "class" : "preptime" }) else None
        self.preptime = self.sanitize(self.preptime)
        txt = soup.find("p", { "class" : "m_content_recette_info"}).text if soup.find("p", { "class" : "m_content_recette_info"}) else None
        self.preptime_unit = self.sanitize(txt).split(" ")[5] if txt else None

        self.cooktime = soup.find("span", { "class" : "cooktime" }).text if soup.find("span", { "class" : "cooktime" }) else None
        self.cooktime_unit = self.sanitize(txt).split(" ")[11] if txt else None

        txt_ing = soup.find("p", { "class" : "m_content_recette_ingredients"})
        self.nb_person = txt_ing.span.string.split(" ")[2] if txt_ing else None
        ingreds = [self.sanitize(i) for i in txt_ing.text.split("-")[1:]] if txt_ing else None
        self.ingredients = []
        if ingreds:
            for i in ingreds:
                if len(i.split(",")) > 1:
                    for elt in i.split(","):
                        self.ingredients.append(Ingredient(self.sanitize(elt)))
                else:
                    self.ingredients.append(Ingredient(i))

        txt_title = soup.find("div", { "class" : "m_content_recette_todo"}).h4.string if soup.find("div", { "class" : "m_content_recette_todo"}) else None
        txt_instructions = soup.find("div", { "class" : "m_content_recette_todo"}).text if soup.find("div", { "class" : "m_content_recette_todo"}) else None
        txt_instructions = self.sanitize(txt_instructions.replace(txt_title, "")) if txt_instructions else None
        self.instructions = txt_instructions.split("Remarques :")[0] if txt_instructions else None
        self.instructions = self.instructions.split("Boisson conseillée :")[0] if self.instructions else None
        self.remarks = txt_instructions.split("Remarques :")[1] if txt_instructions and "Remarques :" in txt_instructions else None
        self.remarks = self.remarks.split("Boisson conseillée :")[0] if self.remarks else None
        self.drink = txt_instructions.split("Boisson conseillée :")[1] if txt_instructions and "Boisson conseillée :" in txt_instructions else None

    def pretty_print(self):
        print("Title: %s" % self.title)
        print("URL: %s" % self.url)
        print("Type de repas: %s" % self.meal_type)
        print("Difficulté: %s" % self.difficulty)
        print("Gamme de prix: %s" % self.price_range)
        print("Image: %s" % self.picture_url)
        print("Temps de préparation: %s %s" % (self.preptime, self.preptime_unit))
        print("Temps de cuisson: %s %s" % (self.cooktime, self.cooktime_unit))
        print("Pour %s personne(s)" % self.nb_person)
        if self.ingredients:
            print("Ingrédients:")
            for i in self.ingredients.text:
                print("- %s" % i)
        else:
            print("Ingredients: None")
        print("Instructions:")
        print(self.instructions)
        print("Remarques:")
        print(self.remarks)
        print("Boisson:")
        print(self.drink)

    def pretty_print_ingredients(self):
        if self.ingredients:
            print("Ingrédients for %s" % self.url)
            for i in self.ingredients:
                print("\t\033[92m%s\t\033[96m%s\t\033[91m%s\033[0m" % (i.quantity, i.unit, i.name))
        else:
            print("Ingredients: None")

    def save_screenshot(self):
        """ Take screenshot of the page and save it (requires phantomjs) """
        script = os.path.join(os.path.dirname(__file__), 'webshot.js')
        call(['phantomjs', script, self.url])


def random_recipe():
    with  open("testing/recipe_engine/good_recipes.txt", "r") as f:
        return Recipe(random.choice(f.readlines()).rstrip("\n"))
