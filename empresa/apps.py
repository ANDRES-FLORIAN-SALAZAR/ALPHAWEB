"""este modulo define la configuracion de la aplicacion empresa."""
from django.apps import AppConfig


class EmpresaConfig(AppConfig):
    """Configuracion de la aplicacion empresa."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "empresa"
