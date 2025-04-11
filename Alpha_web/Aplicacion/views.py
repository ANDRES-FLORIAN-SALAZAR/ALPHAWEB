from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import Persona, Empresa, DocumentoCajaFuerte
import os
import logging
from functools import wraps

# Configurar el logger
logger = logging.getLogger(__name__)

# Función para verificar si un usuario está autenticado
def verificar_autenticacion(request):
    if 'usuario_id' in request.session:
        try:
            return Persona.objects.get(id=request.session['usuario_id'])
        except Persona.DoesNotExist:
            del request.session['usuario_id']
    return None

# Decorador personalizado para verificar si un usuario está autenticado
def requiere_autenticacion(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario = verificar_autenticacion(request)
        if not usuario:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página.')
            return redirect('Inicio_Sesion')  # Corregido: 'Inicio_Sesión' -> 'Inicio_Sesion'
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Función de registro
def Registro(request):
    # Si el usuario ya está autenticado, redirigir a home
    if verificar_autenticacion(request):
        return redirect('home')
        
    if request.method == 'POST':
        logger.info(f"Datos del formulario: {request.POST}")
        
        tipo_registro = request.POST.get('tipo_registro')
        
        if not tipo_registro:
            messages.error(request, "Por favor seleccione un tipo de registro.")
            return redirect('registro')
        
        email = request.POST.get('email') if tipo_registro == 'natural' else request.POST.get('email_empresa')
        
        if email and Persona.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado. Por favor utilice otro o inicie sesión.")
            return redirect('registro')
            
        try:
            if tipo_registro == 'natural':
                return registro_persona_natural(request)
            
        except Exception as e:
            logger.error(f"Error en el registro: {str(e)}")
            messages.error(request, 'Ocurrió un error durante el registro. Por favor intente nuevamente.')
            return redirect('registro')
    
    return render(request, 'Registro.html')

def registro_persona_natural(request):
    nombre_completo = request.POST.get('nombre_completo', '')
    if not nombre_completo:
        messages.error(request, "El nombre completo es obligatorio.")
        return redirect('registro')
    
    partes_nombre = nombre_completo.split()
    nueva_persona = Persona()
    if partes_nombre:
        nueva_persona.nombre = partes_nombre[0]
        if len(partes_nombre) > 1:
            nueva_persona.apellido = ' '.join(partes_nombre[1:])
    
    email = request.POST.get('email', '')
    if not email:
        messages.error(request, "El email es obligatorio.")
        return redirect('registro')
    
    contraseña = request.POST.get('contraseña', '')
    if not contraseña:
        messages.error(request, "La contraseña es obligatoria.")
        return redirect('registro')
    
    nueva_persona.email = email
    nueva_persona.contraseña = make_password(contraseña)
    nueva_persona.edad = request.POST.get('edad') or None
    nueva_persona.telefono = request.POST.get('celular', '')
    nueva_persona.genero = request.POST.get('genero', '')
    nueva_persona.rol = 'Usuario'
    nueva_persona.save()
    
    messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
    return redirect('Inicio_Sesion')


# Página principal
def home(request):
    usuario = verificar_autenticacion(request)
    return render(request, 'home.html', {'usuario': usuario})   

def Planes(request):
    usuario = verificar_autenticacion(request)
    return render(request, 'Planes.html', {'usuario': usuario})

# Función de inicio de sesión
def Inicio_Sesion(request):  # Nombre corregido para consistencia
    if verificar_autenticacion(request):
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        
        if not email or not contraseña:
            messages.error(request, "Por favor complete todos los campos.")
            return render(request, 'Inicio_Sesion.html')
        
        try:
            usuario = Persona.objects.get(email=email)
            
            if check_password(contraseña, usuario.contraseña):
                request.session['usuario_id'] = usuario.id
                request.session.set_expiry(1209600)  # 2 semanas
                
                nombre_usuario = usuario.nombre or usuario.nombre_empresa or usuario.email
                messages.success(request, f'¡Bienvenido, {nombre_usuario}!')
                
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Persona.DoesNotExist:
            messages.error(request, 'No existe un usuario con ese email.')
    
    return render(request, 'Inicio_Sesion.html')

def Contraseñas(request):
    usuario = verificar_autenticacion(request)
    return render(request, 'Contraseñas.html', {'usuario': usuario})

def cerrar_sesion(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
        request.session.flush()
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')

# Vistas para la Caja Fuerte
@requiere_autenticacion
def caja_fuerte(request):
    usuario = verificar_autenticacion(request)
    documentos = DocumentoCajaFuerte.objects.filter(usuario=usuario).order_by('-fecha_subida')
    return render(request, 'CajaFuerte.html', {
        'usuario': usuario,
        'documentos': documentos
    })

@requiere_autenticacion
def subir_documento(request):
    usuario = verificar_autenticacion(request)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        archivo = request.FILES.get('archivo')
        
        if not nombre or not archivo:
            messages.error(request, 'Nombre y archivo son campos requeridos.')
            return redirect('subir_documento')
        
        try:
            DocumentoCajaFuerte.objects.create(
                usuario=usuario,
                nombre=nombre,
                descripcion=request.POST.get('descripcion', ''),
                categoria=request.POST.get('categoria', 'Otros'),
                archivo=archivo
            )
            messages.success(request, '¡Documento subido con éxito!')
            return redirect('caja_fuerte')
        except Exception as e:
            logger.error(f"Error al subir documento: {str(e)}")
            messages.error(request, 'Error al subir el documento. Intente nuevamente.')
    
    return render(request, 'SubirDocumento.html', {'usuario': usuario})

@requiere_autenticacion
def ver_documento(request, documento_id):
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)
    
    try:
        return FileResponse(
            open(documento.archivo.path, 'rb'),
            as_attachment=True,
            filename=os.path.basename(documento.archivo.name)
        )
    except Exception as e:
        logger.error(f"Error al acceder al documento {documento_id}: {str(e)}")
        messages.error(request, 'Error al acceder al documento.')
        return redirect('caja_fuerte')

@requiere_autenticacion
def eliminar_documento(request, documento_id):
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)
    
    if request.method == 'POST':
        try:
            if documento.archivo and os.path.isfile(documento.archivo.path):
                os.remove(documento.archivo.path)
            documento.delete()
            messages.success(request, 'Documento eliminado correctamente.')
        except Exception as e:
            logger.error(f"Error al eliminar documento {documento_id}: {str(e)}")
            messages.error(request, 'Error al eliminar el documento.')
        
        return redirect('caja_fuerte')
    
    return render(request, 'confirmar_eliminar_documento.html', {
        'documento': documento
    })