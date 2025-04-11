from django.urls import path
from Aplicacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('planes/', views.Planes, name='Planes'),
    path('inicio-sesion/', views.Inicio_Sesion, name='inicio_sesion'),
    path('registro/', views.Registro, name='registro'),
    path('contrasenas/', views.Contraseñas, name='contrasenas'),
    path('caja-fuerte/', views.caja_fuerte, name='caja_fuerte'),
    path('caja-fuerte/subir/', views.subir_documento, name='subir_documento'),
    path('caja-fuerte/ver/<int:documento_id>/', views.ver_documento, name='ver_documento'),
    path('caja-fuerte/eliminar/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('registro-empresas/', views.registro_empresa_completo, name='registro_empresas'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)