from django.urls import path
from . import views

app_name = 'empresa'

urlpatterns = [
    path('perfil/', views.perfil_empresa, name='perfil_empresa'),
    path('tipos/', views.tipos_empresa, name='tipos_empresa'),
]
