#! /usr/bin/env python
# coding: utf-8

class Ingredient:
    """ Parse given string to extract a name, a unit and a quantity """

    def __init__(self, s):
        self.text = s
        self.name = None
        self.unit = None
        self.quantity = None

        s = s.replace("0g", "0 g")

        word2num = {
                "un demi" : 1/2,
                "trois-quarts" : 3/4, "trois quarts" : 3/4, "3 quart" : 3/4,
                "un" : 1, "une" : 1,
                "deux" : 2,
                "trois" : 3,
                "quatre" : 4,
                "cinq" : 5,
                "six" : 6,
                "sept" : 7,
                "huit" : 8,
                "neuf" : 9,
                "dix" : 10, "une dizaine" : 10,
                "onze" : 11, "une onzaine" : 11,
                "douze" : 12, "une douzaine" : 12
        }

        word2unit = {
                "quelques gouttes" : "1 g", "un peu" : "1 g", "une pincée" : "1 g", "un soupçon" : "1 g", "une goutte" : "1 g", "un nuage" : "1 g", "un zeste" : "1 g", "un fond" : "1 g",
                "milligramme" : "mg", "milligrammes" : "mg",
                "centigramme" : "cg", "centigrammes" : "cg",
                "decigramme" : "dg", "decigrammes" : "dg",
                "gramme" : "g", "grammes" : "g",
                "kilogramme" : "kg", "kilogrammes" : "kg", "kilo" : "kg", "kilos" : "kg",
                "litre" : "l",
                "cuillères à soupe" : "cuillère à soupe", "cuillerée" : "cuillère à soupe",
                "cuillères à café" : "cuillère à café",
                "verres" : "verre",
                "tranches" : "tranche",
                "gousses" : "gousse",
                "boîtes": "boîte", "boites": "boîte"
        }

        units = [ "mg", "g", "cg", "kg", "l", "cl", "cuillère à soupe", "cuillère à café", "verre", "tranche" , "gousse", "boîte" ]
        
        useless = [ "de" ]

        # step 1: numerize
        for key, val in word2num.items():
            s = s.replace(" " + key + " ", " " + str(val) + " ")
            if s.startswith(key + " ") or s.endswith(" " + key):
                s = s.replace(key, str(val))

        # step 2: unify units
        for key, val in word2unit.items():
            s = s.replace(" " + key + " ", " " + val + " ")
            if s.startswith(key + " ") or s.endswith(" " + key):
                s = s.replace(key, val)

        # step 3: remove useless words
        for w in useless:
            s = s.replace(" " + w, "")

        # step 4: parse
        after_quantity = False
        in_unit = False
        for word in s.split(" "):
            if in_unit:
                self.unit += " " + word
                self.name += " " + word
                for u in units:
                    if self.unit == u:
                        in_unit = False
                        self.name = None
                continue
            if self.quantity:
                after_quantity = True
            try:
                if self.quantity:
                    self.quantity = self.quantity * int(word)
                    self.name = None
                else:
                    self.quantity = int(word)
                    self.name = None
            except:
                if self.quantity and (self.unit or self.name):
                    self.name = self.name + " " + word if self.name else word
                    continue
                if "/" in word:
                    word = word.split("/")
                    try:
                        self.quantity = int(word[0]) / int(word[1])
                    except:
                        pass
                else:
                    if word in units:
                        self.unit = word
                    else:
                        for u in units:
                            if u.split(" ")[0] == word:
                                self.unit = word
                                self.name = word # in case not a unit
                                in_unit = True
                        if after_quantity:
                            after_quantity = False
                            self.name = word
                pass

        if not self.quantity and not self.unit:
            self.name = s

        if self.name == self.unit:
            self.unit = None
