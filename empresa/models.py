from django.db import models
from django.conf import settings

class TipoEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    tipo_empresa = models.ForeignKey(
        TipoEmpresa,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="perfiles"
    )
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.email}"
