from django import template

register = template.Library()

DAY_SLOT = ['Matin', 'Collation', 'Déjeuner', 'Collation', 'Dîner']


@register.filter(name='meal_slot_name')
def meal_slot_name(value):
    return DAY_SLOT[int(value)]