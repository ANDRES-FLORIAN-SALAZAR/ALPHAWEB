"""MOdulo de filtros personalizados para Django."""
from django import template

register = template.Library()
"""FILTROS PERSONALIZADOS PARA USAR EN LAS PLANTILLAS DE DJANGO."""
@register.filter
def endswith(value: str, suffix: str) -> bool:
    """Retorna True si 'value' termina con 'suffix'."""
    try:
        return str(value).lower().endswith(str(suffix).lower())
    except (AttributeError, TypeError):
        return False
