from django import template

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
def shopping_unit(unit):
    units = {
        'g': 'grammes',
        'mg': 'milligrammes',
        'cg': 'centigrammes',
        'dg': 'decigrammes',
        'kg': 'kilogrammes',
        'l': ';otre',
        'cuillère à soupe': 'cuillères à soupe',
        'cuillère à café': 'cuillères à café',
        'tranche': 'tranches',
        'gousse': 'gousses',
        'boîte': 'boîtes',
        'verre': 'verres'
    }

    if unit in units:
        return "(%s)" % units[unit]
    else:
        return ""

@register.filter(name='shopping_amount')
def shopping_amount(amount):
    if amount is None:
        return "1"
    return amount

@register.filter(name="index")
def index(array, key):
    return array[key]
