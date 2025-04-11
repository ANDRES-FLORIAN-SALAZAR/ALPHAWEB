from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator  # Añade esta importación
import os
from django.core.validators import MaxValueValidator, MinValueValidator

class Persona(models.Model):
    GENERO_OPCIONES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Otro', 'Otro'),
        ('Prefiero no decir', 'Prefiero no decir')
    ]

    # Información básica
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    contraseña = models.CharField(max_length=128)  # Longitud adecuada para hash
    edad = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    genero = models.CharField(
        max_length=50,
        choices=GENERO_OPCIONES,
        null=True, 
        blank=True
    )
    rol = models.CharField(
        max_length=50,
        choices=ROL_OPCIONES,
        default='Usuario'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Encriptar contraseña antes de guardar
        if self.contraseña and not self.contraseña.startswith('pbkdf2_sha256$'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


def documento_path(instance, filename):
    # Ruta: documentos/user_id/year/month/filename
    return f'documentos/user_{instance.usuario.id}/{filename}'

class DocumentoCajaFuerte(models.Model):
    CATEGORIAS = [
        ('Personal', 'Personal'),
        ('Laboral', 'Laboral'),
        ('Financiero', 'Financiero'),
        ('Médico', 'Médico'),
        ('Legal', 'Legal'),
        ('Otro', 'Otro')
    ]

    usuario = models.ForeignKey(
        Persona, 
        on_delete=models.CASCADE, 
        related_name='documentos'
    )
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(
        upload_to=documento_path,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png']
        )]
    )
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(
        max_length=100, 
        choices=CATEGORIAS,
        default='Personal'
    )
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tamaño = models.PositiveIntegerField(editable=False)  # en bytes

    def save(self, *args, **kwargs):
        # Calcular tamaño antes de guardar
        if self.archivo:
            self.tamaño = self.archivo.size
        super().save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.archivo.name)

    def tamaño_mb(self):
        return round(self.tamaño / (1024 * 1024), 2) if self.tamaño else 0

    def __str__(self):
        return f"{self.nombre} ({self.categoria}) - {self.usuario}"

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-fecha_subida']