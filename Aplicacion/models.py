"""modelos de aplicación para la gestión de usuarios y documentos."""

from typing import Any, ClassVar

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils.text import get_valid_filename
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager for Persona user model."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: dict[str, object],
    ) -> "Persona":
        if not email:
            raise ValueError("El email es requerido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: dict[str, object],
    ) -> "Persona":
        return self.create_user(email, password, **extra_fields)


class Persona(AbstractUser):
    """Modelo personalizado de usuario."""

    username = None
    email = models.EmailField("email address", unique=True)
    telefono = models.CharField(max_length=15, blank=False)
    edad = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
    )
    genero = models.CharField(
        max_length=50,
        choices=[
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
            ("Prefiero no decir", "Prefiero no decir"),
        ],
        blank=False,
    )
    rol = models.CharField(
        max_length=50,
        choices=[("Usuario", "Usuario"), ("Admin", "Administrador")],
        default="Usuario",
    )

    groups = models.ManyToManyField(
        "auth.Group", related_name="aplicacion_persona_set", verbose_name="grupos",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="aplicacion_persona_set",
        verbose_name="permisos",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    def save(self, *args: object, **kwargs: object) -> None:
        """Guarda el usuario y asegura que la contraseña esté encriptada."""
        # Validar longitud mínima de contraseña
        if self.password and len(self.password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
            
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_username(self) -> str:
        """Devuelve el email como nombre de usuario."""
        return self.email

    def __str__(self) -> str:
        """Representación en cadena del usuario."""
        return f"{self.first_name} {self.last_name} - {self.email}"


def documento_path(instance: "DocumentoCajaFuerte", filename: str) -> str:
    """Genera una ruta válida para el archivo del documento."""
    safe_filename = get_valid_filename(filename)
    return f"documentos/user_{instance.usuario.id}/{safe_filename}"


class DocumentoCajaFuerte(models.Model):
    """Modelo que representa un documento en la caja fuerte."""

    CATEGORIAS: ClassVar[list[tuple[str, str]]] = [
        ("Personal", "Personal"),
        ("Laboral", "Laboral"),
        ("Financiero", "Financiero"),
        ("Medico", "Médico"),
        ("Legal", "Legal"),
        ("Otro", "Otro"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documentos",
    )
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(
        upload_to=documento_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "docm",
                    "xls",
                    "xlsx",
                    "xlsm",
                    "ppt",
                    "pptx",
                    "pptm",
                    "txt",
                    "rtf",
                    "odt",
                    "ods",
                    "odp",
                    "csv",
                    "xml",
                    "json",
                    "html",
                    "htm",
                    "md",
                ],
            ),
        ],
    )
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(
        max_length=100, choices=CATEGORIAS, default="Personal",
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamano = models.PositiveIntegerField(editable=False)

    class Meta:
        """Meta class for DocumentoCajaFuerte model."""

        verbose_name = "Documento Caja Fuerte"
        verbose_name_plural = "Documentos Caja Fuerte"
        ordering: ClassVar[list[str]] = ["-fecha_subida"]

    def __str__(self) -> str:
        """Representación en cadena del documento."""
        return f"Documento {self.id} de usuario {self.usuario}"

    def save(self, *args: object, **kwargs: dict[str, Any]) -> None:
        """Guarda el documento y calcula su tamaño."""
        if self.archivo:
            self.tamano = self.archivo.size
        super().save(*args, **kwargs)

