from django.urls import path
from Aplicacion import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('Planes/', views.Planes, name='Planes'),
    path('Inicio_Sesión/', views.Inicio_Sesión, name='Inicio_Sesión'),
    path('Registro/', views.Registro, name='Registro'),
    path('Contraseñas/', views.Contraseñas, name='Contraseñas'),
    path('CajaFuerte/', views.caja_fuerte, name='CajaFuerte'),
    path('CajaFuerte/subir/', views.subir_documento, name='SubirDocumento'),
    path('CajaFuerte/ver/<int:documento_id>/', views.ver_documento, name='VerDocumento'),
    path('CajaFuerte/eliminar/<int:documento_id>/', views.eliminar_documento, name='EliminarDocumento'),
    path('logout/', views.cerrar_sesion, name='Logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)