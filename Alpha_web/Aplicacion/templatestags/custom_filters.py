from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith_filter(value, arg):
    return str(value).lower().endswith(str(arg).lower())