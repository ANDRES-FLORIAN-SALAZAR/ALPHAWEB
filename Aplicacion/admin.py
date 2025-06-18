"""
Este archivo se utiliza para registrar los modelos de la aplicación en el panel de administración de Django.

Aquí se pueden personalizar las vistas de administración, agregar filtros, campos de búsqueda, etc.
Se registran todos los modelos de la aplicación para que sean accesibles desde el panel de administración.
Se personalizan las vistas de administración para mejorar la experiencia del usuario.
"""

from typing import ClassVar

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import (
    DocumentoCajaFuerte,
    PerfilUsuario,
    Persona,
    TipoEmpresa,
)


@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    """Admin para el modelo TipoEmpresa."""

    list_display: ClassVar[list[str]] = ["nombre", "activo", "fecha_creacion"]
    list_filter: ClassVar[list[str]] = ["activo", "fecha_creacion"]
    search_fields: ClassVar[list[str]] = ["nombre", "descripcion"]
    ordering: ClassVar[list[str]] = ["nombre"]

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    """Admin para el modelo Persona."""

    list_display: ClassVar[list[str]] = ("first_name", "last_name", "email", "telefono", "rol")
    list_filter: ClassVar[list[str]] = ("rol", "genero")
    search_fields: ClassVar[list[str]] = ("first_name", "last_name", "email")
    readonly_fields: ClassVar[list[str]] = ("date_joined", "last_login")
    fieldsets: ClassVar[list[tuple[str, dict]]] = (
        ("Información Personal", {
            "fields": ("first_name", "last_name", "email", "telefono", "edad", "genero"),
        }),
        ("Información de Seguridad", {
            "fields": ("password", "rol"),
        }),
        ("Fechas", {
            "fields": ("date_joined", "last_login"),
        }),
    )

    def get_readonly_fields(self, _request: HttpRequest, obj: Persona | None = None) -> tuple:
        """Devuelve los campos de solo lectura, agregando 'password' si se edita."""
        if obj:
            return (*self.readonly_fields, "password")
        return self.readonly_fields
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """Admin para el modelo PerfilUsuario."""

    list_display: ClassVar[list[str]] = [
        "user", "empresa", "cargo", "departamento", "telefono_extension",
        "es_administrador_empresa", "puede_gestionar_usuarios", "activo",
        "fecha_vinculacion",
    ]
    list_filter: ClassVar[list[str]] = [
        "empresa", "es_administrador_empresa", "puede_gestionar_usuarios",
        "activo", "fecha_vinculacion",
    ]
    search_fields: ClassVar[list[str]] = [
        "user__email", "user__first_name", "user__last_name",
        "empresa__nombre", "cargo", "departamento",
    ]
    ordering: ClassVar[list[str]] = ["-fecha_vinculacion"]
    readonly_fields: ClassVar[list[str]] = ["fecha_vinculacion"]

    fieldsets = (
        ("Usuario y Empresa", {
            "fields": ("user", "empresa"),
        }),
        ("Información Laboral", {
            "fields": ("cargo", "departamento", "telefono_extension"),
        }),
        ("Permisos", {
            "fields": ("es_administrador_empresa", "puede_gestionar_usuarios"),
        }),
        ("Estado", {
            "fields": ("activo",),
        }),
        ("Fechas", {
            "fields": ("fecha_vinculacion",),
            "classes": ("collapse",),
        }),
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Optimiza la consulta usando select_related."""
        return super().get_queryset(request).select_related("user", "empresa")


@admin.register(DocumentoCajaFuerte)
class DocumentoCajaFuerteAdmin(admin.ModelAdmin):
    """Admin para el modelo DocumentoCajaFuerte."""

    list_display: ClassVar[list[str]] = [
        "nombre", "usuario", "categoria", "fecha_subida",
        "tamano_formatted", "descripcion",
    ]
    list_filter: ClassVar[list[str]] = [
        "categoria", "fecha_subida", "usuario__rol",
    ]
    search_fields: ClassVar[list[str]] = [
        "nombre", "descripcion", "usuario__nombre",
        "usuario__apellido", "usuario__email",
    ]
    ordering: ClassVar[list[str]] = ["-fecha_subida"]
    readonly_fields: ClassVar[list[str]] = ["fecha_subida", "tamano"]
    fieldsets: ClassVar[list[tuple[str, dict]]] = [
        ("Información General", {
            "fields": ("nombre", "archivo", "descripcion", "categoria"),
        }),
        ("Usuario", {
            "fields": ("usuario",),
        }),
        ("Información del Sistema", {
            "fields": ("fecha_subida", "tamano"),
            "classes": ("collapse",),
        }),
    ]

    KB: ClassVar[int] = 1024
    MB: ClassVar[int] = 1024 * 1024

    def tamano_formatted(self, obj: DocumentoCajaFuerte) -> str:
        """Formatea el tamaño del archivo en KB o MB."""
        if obj.tamano:
            if obj.tamano < self.KB:
                return f"{obj.tamano} bytes"
            if obj.tamano < self.MB:
                return f"{obj.tamano / self.KB:.1f} KB"
            return f"{obj.tamano / self.MB:.1f} MB"
        return "0 bytes"
