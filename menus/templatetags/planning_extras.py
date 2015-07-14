from django import template

register = template.Library()

DAY_SLOT = ['Déjeuner', 'Dîner']


@register.filter(name='meal_slot_name')
def meal_slot_name(value):
    return DAY_SLOT[int(value)]


@register.filter(name='column_size')
def column_size(value):
    return int(round(12 / value, 0))
