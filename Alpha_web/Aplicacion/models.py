"""este módulo contiene los modelos de la aplicación."""
from typing import ClassVar

from django.contrib.auth.hashers import make_password
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models

"""Este módulo contiene los modelos de la aplicación."""


class Persona(models.Model):
    """
    Modelo que representa a una persona.

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_

    """

    GENERO_OPCIONES: ClassVar[list[tuple[str, str]]] = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro"),
        ("Prefiero no decir", "Prefiero no decir"),
    ]

    ROL_OPCIONES: ClassVar[list[tuple[str, str]]] = [
        ("Usuario", "Usuario"),
        ("Admin", "Administrador"),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    contrasena = models.CharField(max_length=128)
    edad = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
    )
    genero = models.CharField(
        max_length=50,
        choices=GENERO_OPCIONES,
        blank=True,
    )
    rol = models.CharField(
        max_length=50,
        choices=ROL_OPCIONES,
        default="Usuario",
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)

    class Meta:
        """Configuración de metadatos del modelo."""

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self: str) -> str:
        """
        Representa al usuario como una cadena.

        Returns:
            str: Nombre completo y correo electrónico del usuario.

        """
        return f"{self.nombre} {self.apellido} - {self.email}"

    def save(self, *args:list, **kwargs:dict) -> None:
        """Guarda el usuario en la base de datos."""
        if self.contrasena and not self.contrasena.startswith("pbkdf2_sha256$"):
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)



def documento_path(instance:any, filename:str) -> str:
    """
    Genera la ruta para guardar un documento en la caja fuerte.

    Args:
        instance (any): La instancia del modelo que contiene el documento.
        filename (str): El nombre del archivo a guardar.

    Returns:
        str: La ruta completa donde se guardará el documento.

    """
    return f"documentos/user_{instance.usuario.id}/{filename}"

class DocumentoCajaFuerte(models.Model):
    """Modelo que representa un documento en la caja fuerte."""

    CATEGORIAS: ClassVar[list[tuple[str, str]]] = [

        ("Personal", "Personal"),
        ("Laboral", "Laboral"),
        ("Financiero", "Financiero"),
        ("Médico", "Médico"),
        ("Legal", "Legal"),
        ("Otro", "Otro"),
    ]

    usuario = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="documentos",
    )

    nombre = models.CharField(max_length=200)
    archivo = models.FileField(
        upload_to=documento_path,
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "doc", "docx", "xls", "xlsx", "jpg", "jpeg", "png"],
        )],
    )
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(
        max_length=100,
        choices=CATEGORIAS,
        default="Personal",
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamano = models.PositiveIntegerField(editable=False)

    class Meta:
        """Configuración de metadatos del modelo."""

        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering: ClassVar[list[str]] = ["-fecha_subida"]

    def __str__(self) -> str:
        """
        Representa el documento como una cadena.

        Returns:
            str: Descripción del documento.

        """
        return f"Documento {self.id} de usuario {self.usuario}"



    def save(self, *args: list, **kwargs: dict) -> None:
        """Actualiza el tamaño del archivo antes de guardar el modelo."""
        if self.archivo:
            self.tamano = self.archivo.size  # ← CORREGIDO
        super().save(*args, **kwargs)
