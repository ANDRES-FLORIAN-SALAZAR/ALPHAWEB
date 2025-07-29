"""Esta es la configuración de las URLs para la aplicación de empresa."""
from django.urls import path

from . import views

app_name = "empresa"

urlpatterns = [
    path("dashboard/", views.dashboard_empresa, name="dashboard"),
    path("perfil/", views.perfil_empresa, name="perfil"),
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),
    path("planes/", views.planes, name="planes"),
    path("cajaFuerte/", views.caja_fuerte, name="caja_fuerte"),
    path("contrasenas/", views.contrasenas, name="contrasenas"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("subir-documento/", views.subir_documento, name="subir_documento"),
    path("ver-documento/<int:documento_id>/", views.ver_documento, name="ver_documento"),
    path("eliminar-documento/<int:documento_id>/", views.eliminar_documento, name="eliminar_documento"),

    # Nueva URL para cargar ciudades dinámicamente
    path("api/ciudades/", views.obtener_ciudades, name="obtener_ciudades"),
]
