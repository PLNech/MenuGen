from django import template

register = template.Library()

@register.filter(name='is_false_or_none')
def is_false_or_none(arg):
    return arg is False or arg is None