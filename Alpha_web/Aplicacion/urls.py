from django.urls import path
from Aplicacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', views.Registro, name='registro'),
    path('inicio-sesion/', views.Inicio_Sesion, name='Inicio_Sesion'),
    path('planes/', views.Planes, name='Planes'),
    path('caja-fuerte/', views.caja_fuerte, name='CajaFuerte'),
    path('contrasenas/', views.Contrasenas, name='Contrasenas'),
    path('cerrar-sesion/', views.cerrar_sesion, name='Logout'),
    path('caja-fuerte/', views.caja_fuerte, name='caja_fuerte'),
    path('caja-fuerte/subir/', views.subir_documento, name='subir_documento'),
    path('caja-fuerte/ver/<int:documento_id>/', views.ver_documento, name='ver_documento'),
    path('caja-fuerte/eliminar/<int:documento_id>/', views.eliminar_documento, name='eliminar_documento'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)