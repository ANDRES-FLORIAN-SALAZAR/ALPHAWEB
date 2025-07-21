from django.contrib import admin
from .models import TipoEmpresa, PerfilUsuario

@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_empresa', 'telefono')
    search_fields = ('usuario__username', 'tipo_empresa__nombre')
    list_filter = ('tipo_empresa',)
