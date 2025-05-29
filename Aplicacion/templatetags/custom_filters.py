"""
Este módulo implementa un filtro personalizado para Django.

que permite verificar si una cadena termina con un sufijo específico.
"""


from django import template

""" este archivo implementa un filtro personalizado para Django,
que verifica si una cadena termina con un sufijo específico.
Este filtro se puede utilizar en plantillas de Django para realizar comparaciones de cadenas de manera más sencilla.
El filtro se llama 'endswith' y toma dos argumentos: 'value' y 'suffix'.
El argumento 'value' es la cadena que se va a verificar, y 'suffix' es el sufijo que se está buscando.
El filtro devuelve True si 'value' termina con 'suffix', y False en caso contrario.
"""
register = template.Library()

@register.filter
def endswith(value: any, suffix: any) -> bool:
    """Retorna True si 'value' termina con 'suffix'."""
    try:
        return str(value).lower().endswith(str(suffix).lower())
    except (AttributeError, TypeError):
        """
        Maneja excepciones de tipo AttributeError o TypeError durante la verificación.
        """
        return False


