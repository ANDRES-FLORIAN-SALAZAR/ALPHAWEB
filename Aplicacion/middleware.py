"""Módulo de middleware para manejo de errores 404.

Este módulo contiene el middleware Custom404Middleware que se encarga de manejar
errores 404 mostrando una página personalizada.
"""

from collections.abc import Callable

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Código de estado HTTP para página no encontrada
STATUS_NOT_FOUND = 404


class Custom404Middleware:
    """Middleware personalizado para manejar errores 404.

    Este middleware intercepta las respuestas HTTP y muestra una página personalizada
    cuando se detecta un error 404 (página no encontrada).
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        """Inicializa el middleware.

        Args:
            get_response: Función que obtiene la respuesta HTTP
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Procesa la solicitud y maneja los errores 404.

        Args:
            request: La solicitud HTTP entrante

        Returns:
            HttpResponse: La respuesta HTTP procesada
        """
        response = self.get_response(request)

        if response.status_code == STATUS_NOT_FOUND:
            context = {
                "imagen_url": "/static/img/respira_valido.gif",
            }
            return render(request, "404.html", context, status=STATUS_NOT_FOUND)

        return response