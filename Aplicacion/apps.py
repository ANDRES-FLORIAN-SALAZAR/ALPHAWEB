"""Modulo para implementar la configuracion de la aplicacion."""
from django.apps import AppConfig


class AplicacionConfig(AppConfig):
    """Clase para configurar la aplicacion."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "Aplicacion"
