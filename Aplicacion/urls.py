"""
Este módulo contiene las URLs de la aplicación, las cuales son las rutas que se utilizan para acceder a las vistas de la aplicación.

Las URLs son las direcciones que se utilizan para acceder a las diferentes partes de la aplicación web.

Las vistas son funciones que manejan las peticiones HTTP y devuelven respuestas HTTP.

Son responsables de la lógica de negocio y de interactuar con los modelos y plantillas para generar la respuesta adecuada.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Aplicacion import views as aplicacion_views
from empresa import views as empresa_views

app_name = "Aplicacion"

urlpatterns = [
    # Rutas principales de la aplicación 'Aplicacion'
    path("", aplicacion_views.home, name="home"),
    path("registro/", aplicacion_views.registro, name="registro"),

    path("inicio-sesion/", aplicacion_views.inicio_sesion, name="inicio_sesion"),
    path("planes/", aplicacion_views.planes, name="planes"),
    path("cajaFuerte/", aplicacion_views.caja_fuerte, name="caja_fuerte"),
    path("contrasenas/", aplicacion_views.contrasenas, name="contrasenas"),
    path("cerrar-sesion/", aplicacion_views.cerrar_sesion, name="cerrar_sesion"),
    path("subir-documento/", aplicacion_views.subir_documento, name="subir_documento"),
    path("ver-documento/<int:documento_id>/", aplicacion_views.ver_documento, name="ver_documento"),
    path("eliminar-documento/<int:documento_id>/", aplicacion_views.eliminar_documento, name="eliminar_documento"),

    # Rutas de la aplicación 'empresa'
    # Registro
    path("empresa/registro/", empresa_views.registro_usuario, name="registro_usuario"),

    # Listado y detalles
    path("empresa/empresas/", empresa_views.listar_empresas, name="listar_empresas"),
    path("empresa/empresa/<int:empresa_id>/", empresa_views.detalle_empresa, name="detalle_empresa"),

    # APIs
    path("empresa/api/empresas/segmento/", empresa_views.api_empresas_por_segmento, name="api_empresas_por_segmento"),
    path("empresa/api/tipos-empresa/", empresa_views.api_tipos_empresa, name="api_tipos_empresa"),
    path("empresa/api/empresa/<int:empresa_id>/", empresa_views.api_empresa_detalle, name="api_empresa_detalle"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
