"""Models for the empresa app, defining company types, segments, and companies."""

from django.db import models


class TipoEmpresa(models.Model):
    """Model representing a type of company."""

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        """Meta options for TipoEmpresa."""

        verbose_name = "Tipo de Empresa"
        verbose_name_plural = "Tipos de Empresa"

    def __str__(self) -> str:
        """Return the string representation of the TipoEmpresa."""
        return self.nombre
class Segmento(models.Model):
    """Model representing a company segment."""

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        """Meta options for Segmento."""

        verbose_name = "Segmento"
        verbose_name_plural = "Segmentos"

    def __str__(self) -> str:
        """Return the string representation of the Segmento."""
        return self.nombre
class Empresa(models.Model):
    """Model representing a company."""

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo_empresa = models.ForeignKey(TipoEmpresa, on_delete=models.SET_NULL, null=True, blank=True)
    segmento = models.ForeignKey(Segmento, on_delete=models.SET_NULL, null=True, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    class Meta:
        """Meta options for Empresa."""

        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self) -> str:
        """Return the string representation of the Empresa."""
        return self.nombre
