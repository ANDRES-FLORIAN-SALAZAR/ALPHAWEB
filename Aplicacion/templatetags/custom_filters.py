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


@register.filter
def get_file_type(value: str) -> str:
    """Retorna una descripción del tipo de archivo basado en su extensión."""
    value = str(value).lower()

    # Documentos de Microsoft Office
    if value.endswith((".doc", ".docx", ".docm")):
        return "Documento de Word"
    if value.endswith((".xls", ".xlsx", ".xlsm")):
        return "Hoja de Excel"
    if value.endswith((".ppt", ".pptx", ".pptm")):
        return "Presentación de PowerPoint"

    # Otros formatos de documento
    if value.endswith(".pdf"):
        return "Documento PDF"
    if value.endswith(".txt"):
        return "Texto plano"
    if value.endswith(".rtf"):
        return "Rich Text Format"
    if value.endswith((".odt", ".ods", ".odp")):
        return "Formato OpenDocument"
    if value.endswith(".csv"):
        return "Archivo CSV"
    if value.endswith((".xml", ".json")):
        return "Archivo de datos"
    if value.endswith((".html", ".htm")):
        return "Documento HTML"
    if value.endswith(".md"):
        return "Documento Markdown"

    # Otros formatos
    return "Archivo"
