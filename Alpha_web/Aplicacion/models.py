from django.db import models
from django.contrib.auth.hashers import make_password
import os

class Persona(models.Model):
    # Información básica (Usuario y Administrador)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    contraseña = models.CharField(max_length=100)  # Se encriptará antes de guardar
    edad = models.IntegerField(null=True, blank=True)  # Campo opcional
    genero = models.CharField(
        max_length=50,
        choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')],
        null=True, blank=True
    )

    # Información de empresa
    nombre_empresa = models.CharField(max_length=100, null=True, blank=True)  # Opcional
    nit = models.CharField(max_length=20, null=True, blank=True)  # Opcional, removed unique constraint
    direccion_empresa = models.CharField(max_length=255, null=True, blank=True)  # Opcional

    # Rol del usuario (Administrador, Empresa, Usuario)
    rol = models.CharField(
        max_length=50,
        choices=[('Administrador', 'Administrador'), ('Empresa', 'Empresa'), ('Usuario', 'Usuario')],
        default='Usuario'
    )
    
    def save(self, *args, **kwargs):
        # Encriptar contraseña antes de guardar
        if self.contraseña and not self.contraseña.startswith('pbkdf2_sha256$'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.rol == 'Empresa':
            return f"{self.nombre_empresa} - {self.rol}"
        return f"{self.nombre} {self.apellido} - {self.rol}"

def documento_path(instance, filename):
    # Crea una ruta personalizada para cada archivo
    return f'documentos/{instance.usuario.id}/{filename}'

class Empresas(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    nit = models.CharField(max_length=20, unique=True)
    direccion_empresa = models.CharField(max_length=255)
    telefono_empresa = models.CharField(max_length=15)
    email_empresa = models.EmailField()
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='empresas')

    def __str__(self):
        return self.nombre_empresa
    
class DocumentoCajaFuerte(models.Model):
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to=documento_path)
    descripcion = models.TextField(blank=True, null=True)
    categoria = models.CharField(max_length=100, 
                              choices=[
                                  ('Personal', 'Personal'),
                                  ('Laboral', 'Laboral'),
                                  ('Financiero', 'Financiero'),
                                  ('Médico', 'Médico'),
                                  ('Legal', 'Legal'),
                                  ('Otro', 'Otro')
                              ],
                              default='Personal')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    def filename(self):
        return os.path.basename(self.archivo.name)
    
    def __str__(self):
        return f"{self.nombre} - {self.usuario}"