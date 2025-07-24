"""
URL configuration for Alpha_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from Aplicacion.views import custom_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Aplicacion.urls", namespace="Aplicacion")),
    path("empresa/", include("empresa.urls")),  # URLs específicas de empresa
]

# Configuración de errores personalizados
handler404 = custom_404

# Configuración para servir archivos estáticos en desarrollo
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    urlpatterns += [
        path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
        path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
