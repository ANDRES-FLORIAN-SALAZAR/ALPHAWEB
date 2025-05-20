from django import template

register = template.Library()

@register.filter
def endswith(value, suffix):
    """Retorna True si 'value' termina con 'suffix'."""
    try:
        return str(value).lower().endswith(str(suffix).lower())
    except:
        return False
