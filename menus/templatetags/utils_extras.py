import logging

from django import template
from django.template.defaultfilters import slugify
from unidecode import unidecode

logger = logging.getLogger("menus")
register = template.Library()


@register.filter(name='is_false_or_none')
def is_false_or_none(arg):
    return arg is False or arg is None


@register.filter(name='range_to')
def range_to(begin, end):
    return range(begin, end)


@register.filter(name='stepped_range_to')
def stepped_range_to(begin, end):
    return [x / 10.0 for x in range(begin, end)]


@register.filter(name='shopping_unit')
def shopping_unit(unit, units):
    amount = units[unit]
    plural = amount and amount > 1
    if plural:
        units = {
            'g': 'grammes',
            'dg': 'décigrammes',
            'cg': 'centigrammes',
            'mg': 'milligrammes',
            'kg': 'kilogrammes',
            'l': 'litres',
            'dl': 'décilitres',
            'cl': 'centilitres',
            'ml': 'millilitres',
            'cuillère à soupe': 'cuillères à soupe',
            'cuillère à café': 'cuillères à café',
            'tranche': 'tranches',
            'gousse': 'gousses',
            'boîte': 'boîtes',
            'verre': 'verres'
        }
    else:
        units = {
            'g': 'gramme',
            'dg': 'décigramme',
            'cg': 'centigramme',
            'mg': 'milligramme',
            'kg': 'kilogramme',
            'l': 'litre',
            'dl': 'décilitre',
            'cl': 'centilitre',
            'ml': 'millilitre',
            'cuillère à soupe': 'cuillère à soupe',
            'cuillère à café': 'cuillère à café',
            'tranche': 'tranche',
            'gousse': 'gousse',
            'boîte': 'boîte',
            'verre': 'verre'
        }
    if unit in units:
        return "%s" % units[unit]
    else:
        return ""


@register.filter(name='shopping_amount')
def shopping_amount(amount):
    if amount is None:
        return "1"
    if amount % 1 == 0:
        return '%i' % amount
    return '%s' % amount


@register.filter(name="index")
def index(array, key):
    return array[key]


@register.filter(name="slug")
def slug(value):
    return slugify(unidecode(value))

@register.filter(name="recipeurl")
def recipeurl(url):
    return "http://" + url.split("//")[1]
