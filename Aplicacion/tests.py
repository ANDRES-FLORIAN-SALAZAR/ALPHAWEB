"""Test cases for the Aplicacion app registration functionality."""

import pytest
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

# Ensure the custom user model is used and has the required fields.
# If not, you may need to create a custom user model in your app's models.py.


class UrlConfigurationError(Exception):
    """Exception raised for errors in the URL configuration."""

class RegistroTests(TestCase):
    """Test cases for user registration in the Aplicacion app."""

    def setUp(self) -> None:
        """Set up the test client and URLs for registration and plans."""
        self.client = Client()
        try:
            self.registro_url = reverse("Aplicacion:registro")
            self.planes_url = reverse("Aplicacion:planes")
        except Exception as e:
            error_message = "Required URL name missing or misconfigured."
            raise UrlConfigurationError(error_message) from e

    def test_registro_contrasenas_no_coinciden(self) -> None:
        """Test registration fails when passwords do not match."""
        data = {
            "tipo_usuario": "natural",
            "nombre_completo": "Juan Perez",
            "email": "juan.perez+test2@gmail.com",
            "password1": "Test123!Test",
            "password2": "ContraseñaDiferente",
            "celular": "3143757171",
            "genero": "Masculino",
        }
        response = self.client.post(self.registro_url, data)
        assert response.status_code == HttpResponseRedirect.status_code  # noqa: S101
        assert response.url == self.registro_url  # noqa: S101
        with pytest.raises(get_user_model().DoesNotExist):
            get_user_model().objects.get(email="juan.perez+test2@gmail.com")
