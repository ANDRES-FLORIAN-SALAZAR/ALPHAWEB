"""
este modulo contiene las urls de la aplicacion, las cuales son las rutas que se utilizan para acceder a las vistas de la aplicacion.

las urls son las direcciones que se utilizan para acceder a las diferentes partes de la aplicacion web.

"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Aplicacion import views

""" en este archivo se encuentran las vistas de la aplicacion, las cuales son funciones que manejan las peticiones HTTP

y devuelven respuestas HTTP.

Las vistas son responsables de la logica de negocio y de interactuar con los modelos

y plantillas para generar la respuesta adecuada."""

urlpatterns = [
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
