"""Models for the Aplicacion app."""

from typing import Any, ClassVar

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils.text import get_valid_filename
from django.utils.translation import gettext_lazy as _

# ==================== MODELOS DE EMPRESA ====================

class TipoEmpresa(models.Model):
    """Modelo que representa un tipo de empresa."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for TipoEmpresa model."""

        verbose_name = "Tipo de Empresa"
        verbose_name_plural = "Tipos de Empresa"
        ordering: ClassVar[list[str]] = ["nombre"]

    def __str__(self) -> str:
        """Return the string representation of the TipoEmpresa instance."""
        return self.nombre
class SegmentoEmpresa(models.Model):
    """Modelo que representa un segmento de empresa."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for SegmentoEmpresa model."""

        verbose_name = "Segmento de Empresa"
        verbose_name_plural = "Segmentos de Empresa"
        ordering: ClassVar[list[str]] = ["nombre"]

    def __str__(self) -> str:
        """Return the string representation of the SegmentoEmpresa instance."""
        return self.nombre

class Empresa(models.Model):
    """Modelo que representa una empresa."""

    TAMANO_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("MICRO", "Microempresa (1-10 empleados)"),
        ("PEQUENA", "Pequeña empresa (11-50 empleados)"),
        ("MEDIANA", "Mediana empresa (51-250 empleados)"),
        ("GRANDE", "Gran empresa (251+ empleados)"),
    ]

    nombre = models.CharField(max_length=200, unique=True)
    nit = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=250)
    tipo_empresa = models.ForeignKey(TipoEmpresa, on_delete=models.PROTECT)
    segmento = models.ForeignKey(SegmentoEmpresa, on_delete=models.PROTECT)
    tamano = models.CharField(max_length=10, choices=TAMANO_CHOICES)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100, default="Colombia")
    sitio_web = models.URLField(blank=True)
    descripcion = models.TextField(blank=True)
    numero_empleados = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    requiere_autenticacion_2fa = models.BooleanField(default=False)
    politica_contrasenas_estricta = models.BooleanField(default=True)

    class Meta:
        """Meta options for Empresa model."""

        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering: ClassVar[list[str]] = ["nombre"]

    def __str__(self) -> str:
        """Return the string representation of the Empresa instance."""
        return f"{self.nombre} ({self.nit})"

    def get_numero_usuarios(self) -> int:
        """Devuelve el número de usuarios asociados a la empresa."""
        return self.perfilusuario_set.count()

class CustomUserManager(BaseUserManager):
    """Custom manager for Persona user model."""

    def create_user(self, email: str, password: str | None = None, **extra_fields: dict[str, object]) -> "Persona":
        """Create and return a user with the given email and password."""
        error_msg = "El email es requerido"
        if not email:
            raise ValueError(error_msg)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    from typing import Optional

    def create_superuser(self, email: str, password: str | None = None, **extra_fields: dict[str, object]) -> "Persona":
        """Create and return a superuser with the given email and password."""
        return self.create_user(email, password, **extra_fields)

class Persona(AbstractUser):
    """Modelo personalizado de usuario."""

    username = None
    email = models.EmailField(_("email address"), unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    edad = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    genero = models.CharField(
        max_length=50,
        choices=[
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
            ("Prefiero no decir", "Prefiero no decir"),
        ],
        blank=True,
    )
    rol = models.CharField(
        max_length=50,
        choices=[("Usuario", "Usuario"), ("Admin", "Administrador")],
        default="Usuario",
    )

    groups = models.ManyToManyField("auth.Group", related_name="aplicacion_persona_set", verbose_name="grupos")
    user_permissions = models.ManyToManyField("auth.Permission", related_name="aplicacion_persona_set", verbose_name="permisos")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["first_name", "last_name"]

    def save(self, *args: object, **kwargs: object) -> None:
        """Override save to hash password if needed."""
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def get_username(self) -> str:
        """Return the email as username."""
        return self.email

    def __str__(self) -> str:
        """Return the string representation of the Persona instance."""
        return f"{self.first_name} {self.last_name} - {self.email}"

class PerfilUsuario(models.Model):
    """Modelo que representa el perfil de usuario en una empresa."""

    user = models.OneToOneField(Persona, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True)
    telefono_extension = models.CharField(max_length=10, blank=True)
    es_administrador_empresa = models.BooleanField(default=False)
    puede_gestionar_usuarios = models.BooleanField(default=False)
    fecha_vinculacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        """Meta options for PerfilUsuario model."""

        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering: ClassVar[list[str]] = ["user"]

    def __str__(self) -> str:
        """Return the string representation of the PerfilUsuario instance."""
        return f"{self.user} - {self.empresa}"

def documento_path(instance: "DocumentoCajaFuerte", filename: str) -> str:
    """Return the upload path for a user's document."""
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

    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="documentos")
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(
        upload_to=documento_path,
        validators=[FileExtensionValidator(
            allowed_extensions=[
                "pdf", "doc", "docx", "docm", "xls", "xlsx", "xlsm",
                "ppt", "pptx", "pptm", "txt", "rtf", "odt", "ods",
                "odp", "csv", "xml", "json", "html", "htm", "md",
            ],
        )],
    )
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS, default="Personal")
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamano = models.PositiveIntegerField(editable=False)

    class Meta:
        """Meta options for DocumentoCajaFuerte model."""

        verbose_name = "Documento Caja Fuerte"
        verbose_name_plural = "Documentos Caja Fuerte"
        ordering: ClassVar[list[str]] = ["-fecha_subida"]

    def __str__(self) -> str:
        """Return the string representation of the DocumentoCajaFuerte instance."""
        return f"Documento {self.id} de usuario {self.usuario}"

    def save(self, *args: object, **kwargs: dict[str, Any]) -> None:
        """Override save to set file size."""
        if self.archivo:
            self.tamano = self.archivo.size
        super().save(*args, **kwargs)
