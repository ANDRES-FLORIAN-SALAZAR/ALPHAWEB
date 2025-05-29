"""
apps.py.

este archivo se utiliza para configurar la aplicación Django.

"""

from django.apps import AppConfig

"""
Configuración de la aplicación Django.

Esta clase hereda de AppConfig y define la configuración de la aplicación.

    Attributes:
        default_auto_field (str): Tipo de campo automático por defecto.
        name (str): Nombre de la aplicación.

    Methods:
        default_auto_field (str): Tipo de campo automático por defecto.

        name (str): Nombre de la aplicación.

    Methods:
    __init__(self, *args, **kwargs): Inicializa la configuración de la aplicación.
    ready(self): Método llamado cuando la aplicación está lista.
"""
class AplicacionConfig(AppConfig):
    """Configuración de la aplicación Django."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "Aplicacion"
