"""modelos de aplicación para la gestión de usuarios y documentos."""

from typing import Any, ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.text import get_valid_filename


class CustomUserManager(BaseUserManager):
    """Custom manager for Persona user model."""

    def create_user(
        self, email: str, password: str | None = None, **extra_fields: dict[str, object],
    ) -> "Persona":
        """Crea y devuelve un usuario con el correo electrónico y la contraseña especificados."""
        if not email:
            error_msg = "El campo de correo electrónico es obligatorio."
            raise ValueError(error_msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields: dict[str, object],
    ) -> "Persona":
        """Crea y devuelve un superusuario con el correo electrónico y la contraseña especificados."""
        return self.create_user(email, password, **extra_fields)


class Persona(AbstractUser):
    """Modelo personalizado de usuario que soporta tanto personas naturales como empresas."""

    # Campos comunes para todos los usuarios
    username = None
    email = models.EmailField("Correo electrónico", unique=True)
    telefono = models.CharField("Teléfono", max_length=15, blank=True, default="")

    # Campos específicos para personas naturales
    edad = models.PositiveIntegerField(
        "Edad",
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
    )
    genero = models.CharField(
        "Género",
        max_length=50,
        choices=[
            ("", "Seleccione una opción"),
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
            ("Prefiero no decir", "Prefiero no decir"),
        ],
        blank=True,
        default="",
    )

    # Campos específicos para empresas
    es_empresa = models.BooleanField("¿Es empresa?", default=False)
    razon_social = models.CharField("Razón Social", max_length=200, blank=True, default="")
    nit = models.CharField("NIT", max_length=20, blank=True, null=True, unique=True)
    direccion = models.TextField("Dirección", blank=True, default="")
    representante_legal = models.CharField("Representante Legal", max_length=200, blank=True, default="")
    sitio_web = models.URLField("Sitio Web", blank=True, default="")

    # Campos adicionales para empresas
    empresa_tipo = models.CharField("Tipo de Empresa", max_length=100, blank=True, default="")
    empresa_segmento = models.CharField("Segmento de Empresa", max_length=100, blank=True, default="")
    empresa_tamano = models.CharField("Tamaño de Empresa", max_length=50, blank=True, default="")
    empresa_num_empleados = models.PositiveIntegerField("Número de Empleados", default=0)
    empresa_pais = models.CharField("País de la Empresa", max_length=100, blank=True, default="")
    empresa_ciudad = models.CharField("Ciudad de la Empresa", max_length=100, blank=True, default="")
    empresa_descripcion = models.TextField("Descripción de la Empresa", blank=True, default="")

    # Campos comunes
    rol = models.CharField(
        "Rol",
        max_length=50,
        choices=[("Usuario", "Usuario"), ("Admin", "Administrador")],
        default="Usuario",
    )
    fecha_registro = models.DateTimeField("Fecha de registro", auto_now_add=True)
    ultimo_acceso = models.DateTimeField("Último acceso", auto_now=True)

    # Configuración de permisos
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="aplicacion_persona_set",
        verbose_name="grupos",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="aplicacion_persona_set",
        verbose_name="permisos",
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ()

    class Meta:
        """Configuración de metadatos del modelo Persona."""

        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ("-fecha_registro",)
        db_table = "Aplicacion_persona"

    def __str__(self) -> str:
        """Retorna una representación legible del usuario."""
        if self.es_empresa and self.razon_social:
            return f"{self.razon_social} (Empresa)"
        return self.get_full_name() or self.email

    def get_full_name(self) -> str:
        """Devuelve el nombre completo del usuario."""
        if self.es_empresa and self.razon_social:
            return self.razon_social
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.email

    def get_short_name(self) -> str:
        """Devuelve el nombre corto del usuario (solo el primer nombre)."""
        if self.es_empresa and self.razon_social:
            return self.razon_social
        return self.first_name or self.email.split("@")[0]

    def save(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        """Guarda el usuario en la base de datos."""
        # Asegurar que el email siempre esté en minúsculas
        self.email = self.email.lower().strip()

        # Si es un superusuario, asegurarse de que tenga los permisos necesarios
        if self.is_superuser:
            self.is_staff = True
            self.is_active = True
            self.rol = "Admin"

        super().save(*args, **kwargs)

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
