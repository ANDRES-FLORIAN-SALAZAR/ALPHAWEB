from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class TipoEmpresa(models.Model):
    """Tipos de empresa (Pública, Privada, etc.)"""

    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Tipo de Empresa"
        verbose_name_plural = "Tipos de Empresa"

class PerfilEmpresa(models.Model):
    """Perfil específico para empresas"""

    SEGMENTO_CHOICES = [
        ("tecnologia", "Tecnología"),
        ("salud", "Salud"),
        ("educacion", "Educación"),
        ("finanzas", "Finanzas"),
        ("retail", "Retail"),
        ("manufactura", "Manufactura"),
        ("logistica", "Logística"),
        ("energia", "Energía"),
        ("construccion", "Construcción"),
        ("turismo", "Turismo"),
        ("entretenimiento", "Entretenimiento"),
        ("otros", "Otros"),
    ]

    TAMAÑO_CHOICES = [
        ("micro", "Microempresa (1-10 empleados)"),
        ("pequena", "Pequeña empresa (11-50 empleados)"),
        ("mediana", "Mediana empresa (51-250 empleados)"),
        ("grande", "Gran empresa (251+ empleados)"),
    ]

    # Relación con el usuario
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil_empresa")

    # Información básica de la empresa
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la Empresa")
    nit = models.CharField(max_length=50, unique=True, verbose_name="NIT")
    razon_social = models.CharField(max_length=255, verbose_name="Razón Social")
    tipo = models.ForeignKey(TipoEmpresa, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Empresa")
    segmento = models.CharField(max_length=50, choices=SEGMENTO_CHOICES, verbose_name="Segmento")
    tamaño = models.CharField(max_length=20, choices=TAMAÑO_CHOICES, verbose_name="Tamaño")

    # Ubicación
    pais = models.CharField(max_length=10, verbose_name="País")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")

    # Información adicional
    sitio_web = models.URLField(blank=True, null=True, verbose_name="Sitio Web")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    numero_empleados = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Número de Empleados")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono Empresarial")

    # Configuraciones de seguridad
    requiere_2fa = models.BooleanField(default=False, verbose_name="Requiere 2FA")
    politica_estricta = models.BooleanField(default=False, verbose_name="Política Estricta")

    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} - {self.nit}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} ({self.razon_social})"

    class Meta:
        verbose_name = "Perfil de Empresa"
        verbose_name_plural = "Perfiles de Empresa"
        ordering = ["-fecha_creacion"]
