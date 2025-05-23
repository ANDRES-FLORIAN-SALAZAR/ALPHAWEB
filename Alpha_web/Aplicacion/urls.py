from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Aplicacion import views

""" en este archivo se encuentran las vistas de la aplicacion, las cuales son funciones que manejan las peticiones HTTP

y devuelven respuestas HTTP.

Las vistas son responsables de la logica de negocio y de interactuar con los modelos y plantillas para generar la respuesta adecuada."""

urlpatterns = [
    path("", views.home, name="home"),
    path("registro/", views.Registro, name="registro"),
    path("inicio-sesion/", views.Inicio_Sesion, name="Inicio_Sesion"),
    path("planes/", views.Planes, name="Planes"),
    path("cajaFuerte/", views.caja_fuerte, name="CajaFuerte"),
    path("contrasenas/", views.Contrasenas, name="Contrasenas"),
    path("cerrar-sesion/", views.cerrar_sesion, name="Logout"),
    path("subir-documento/", views.subir_documento, name="SubirDocumento"),
    path("ver-documento/<int:documento_id>/", views.ver_documento, name="VerDocumento"),
    path("eliminar-documento/<int:documento_id>/", views.eliminar_documento, name="EliminarDocumento"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
