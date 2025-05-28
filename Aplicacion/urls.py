"""Modulo para administrar las URLs de la aplicacion."""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Aplicacion import views

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.registro, name="registro"),
    path("inicio-sesion/", views.inicio_sesion, name="inicio_sesion"),
    path("planes/", views.planes, name="planes"),
    path("cajaFuerte/", views.caja_fuerte, name="caja_fuerte"),
    path("contrasenas/", views.contrasenas, name="contrasenas"),
    path("cerrar-sesion/", views.cerrar_sesion, name="cerrar_sesion"),
    path("subir-documento/", views.subir_documento, name="subir_documento"),
    path("ver_documento/<int:documento_id>/", views.ver_documento, name="ver_documento"),
    path("eliminar-documento/<int:documento_id>/", views.eliminar_documento, name="eliminar_documento"),
    path("descargar-documento/<int:documento_id>/", views.descargar_documento, name="descargar_documento"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
