"""
apps.py
este archivo se utiliza para configurar la aplicación Django.
La clase AplicacionConfig hereda de AppConfig y define la configuración de la aplicacion.
"""

from django.apps import AppConfig


class AplicacionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Aplicacion"
