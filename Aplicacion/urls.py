"""
URLs para la aplicación Aplicacion.
"""

from django.urls import path

from . import views

app_name = "Aplicacion"

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),
    path("planes/", views.planes, name="planes"),
    path("cajaFuerte/", views.caja_fuerte, name="caja_fuerte"),
    path("contrasenas/", views.contrasenas, name="contrasenas"),
    path("cambiar-contrasena/", views.cambiar_contrasena, name="cambiar_contrasena"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("subir-documento/", views.subir_documento, name="subir_documento"),
    path("ver-documento/<int:documento_id>/", views.ver_documento, name="ver_documento"),
    path("eliminar-documento/<int:documento_id>/", views.eliminar_documento, name="eliminar_documento"),
]
