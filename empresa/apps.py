"""Módulo de configuración de la aplicación Empresa."""
from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    """Configuración de la aplicación Empresa."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "empresa"
    verbose_name = "Empresa"
