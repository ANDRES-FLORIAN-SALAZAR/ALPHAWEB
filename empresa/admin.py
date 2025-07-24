from django.contrib import admin

from .models import PerfilEmpresa, TipoEmpresa


@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "descripcion"]
    search_fields = ["nombre"]

@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "nit",
        "tipo",
        "segmento",
        "tamaño",
        "activo",
        "fecha_creacion",
    ]

    list_filter = [
        "tipo",
        "segmento",
        "tamaño",
        "activo",
        "verificado",
        "fecha_creacion",
    ]

    search_fields = [
        "nombre",
        "nit",
        "razon_social",
        "usuario__email",
    ]

    readonly_fields = ["fecha_creacion", "fecha_actualizacion"]

    fieldsets = (
        ("Información Básica", {
            "fields": ("usuario", "nombre", "nit", "razon_social"),
        }),
        ("Clasificación", {
            "fields": ("tipo", "segmento", "tamaño", "numero_empleados"),
        }),
        ("Ubicación", {
            "fields": ("pais", "ciudad", "direccion"),
        }),
        ("Contacto", {
            "fields": ("telefono", "sitio_web"),
        }),
        ("Descripción", {
            "fields": ("descripcion",),
        }),
        ("Configuración de Seguridad", {
            "fields": ("requiere_2fa", "politica_estricta"),
        }),
        ("Estado", {
            "fields": ("activo", "verificado", "fecha_creacion", "fecha_actualizacion"),
        }),
    )
