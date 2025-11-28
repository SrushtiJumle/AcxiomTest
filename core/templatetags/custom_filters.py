from django import template

register = template.Library()

@register.filter
def eq(value, arg):
    return value == arg
