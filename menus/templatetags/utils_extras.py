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