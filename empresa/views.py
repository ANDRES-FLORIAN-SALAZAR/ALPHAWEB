from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import TipoEmpresa, PerfilUsuario

@login_required
def perfil_empresa(request):
    perfil = PerfilUsuario.objects.get(usuario=request.user)
    return render(request, 'empresa/perfil_empresa.html', {'perfil': perfil})

@login_required
def tipos_empresa(request):
    tipos = TipoEmpresa.objects.all()
    return render(request, 'empresa/tipos_empresa.html', {'tipos': tipos})
