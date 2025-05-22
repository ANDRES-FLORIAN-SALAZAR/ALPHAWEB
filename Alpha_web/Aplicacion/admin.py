"""
Este archivo se utiliza para registrar los modelos de la aplicación en el panel de administración de Django.

Aquí se pueden personalizar las vistas de administración, agregar filtros, campos de búsqueda, etc.

En este caso, se registra el modelo Persona para que sea accesible desde el panel de administración.

Se recomienda personalizar la vista de administración para mejorar la experiencia del usuario.
"""
from django.contrib import admin

from .models import Persona

admin.site.register(Persona)
