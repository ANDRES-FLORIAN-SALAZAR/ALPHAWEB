"""
Este archivo se utiliza para registrar los modelos de la aplicación en el panel de administración de Django.

Aquí se pueden personalizar las vistas de administración, agregar filtros, campos de búsqueda, etc.
Se registran todos los modelos de la aplicación para que sean accesibles desde el panel de administración.
Se personalizan las vistas de administración para mejorar la experiencia del usuario.
"""


from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import DocumentoCajaFuerte, Persona


@admin.register(DocumentoCajaFuerte)
class DocumentoCajaFuerteAdmin(admin.ModelAdmin):
    """Admin para el modelo DocumentoCajaFuerte."""

    list_display = ("nombre", "categoria", "fecha_subida", "usuario")
    list_filter = ("categoria", "fecha_subida")
    search_fields = ("nombre", "usuario__email")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Obtiene el queryset filtrado por el usuario."""
        return super().get_queryset(request)

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    """Admin para el modelo Persona."""

    list_display = ("email", "first_name", "last_name", "telefono")
    search_fields = ("email", "first_name", "last_name")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Obtiene el queryset filtrado por el usuario."""
        return super().get_queryset(request).filter(is_active=True)

try:
    from django.contrib.auth.models import User
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
