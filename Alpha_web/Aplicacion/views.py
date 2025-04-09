from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth.hashers import check_password, make_password
from .models import Persona, DocumentoCajaFuerte
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
            return redirect('Inicio_Sesión')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Función de registro
def Registro(request):
    # Si el usuario ya está autenticado, redirigir a home
    if verificar_autenticacion(request):
        return redirect('home')
        
    if request.method == 'POST':
        # Para depuración
        print("Datos del formulario:", request.POST)
        logger.info(f"Datos del formulario: {request.POST}")
        
        # Procesar el formulario
        tipo_registro = request.POST.get('tipo_registro')
        
        if not tipo_registro:
            messages.error(request, "Por favor seleccione un tipo de registro.")
            return redirect('Registro')  # Redirigir a la misma página en caso de error
        
        # Verificar si el email ya existe
        email = request.POST.get('email') if tipo_registro == 'natural' else request.POST.get('email_empresa')
        
        if email and Persona.objects.filter(email=email).exists():
            messages.error(request, "El email ya está registrado. Por favor utilice otro o inicie sesión.")
            return redirect('Registro')  # Redirigir a la misma página en caso de error
            
        # Crear una nueva persona
        nueva_persona = Persona()
        
        try:
            if tipo_registro == 'natural':
                nombre_completo = request.POST.get('nombre_completo', '')
                if not nombre_completo:
                    messages.error(request, "El nombre completo es obligatorio.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                # Dividir nombre y apellido
                partes_nombre = nombre_completo.split()
                if len(partes_nombre) > 0:
                    nueva_persona.nombre = partes_nombre[0]
                    if len(partes_nombre) > 1:
                        nueva_persona.apellido = ' '.join(partes_nombre[1:])
                
                email = request.POST.get('email', '')
                if not email:
                    messages.error(request, "El email es obligatorio.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                contraseña = request.POST.get('contraseña', '')
                if not contraseña:
                    messages.error(request, "La contraseña es obligatoria.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                nueva_persona.email = email
                nueva_persona.contraseña = make_password(contraseña)  # Encriptar la contraseña antes de guardar
                nueva_persona.edad = request.POST.get('edad') if request.POST.get('edad') else None
                nueva_persona.telefono = request.POST.get('celular', '')
                nueva_persona.genero = request.POST.get('genero', '')
                nueva_persona.rol = 'Usuario'
            
            elif tipo_registro == 'empresa':
                nombre_empresa = request.POST.get('nombre_empresa', '')
                if not nombre_empresa:
                    messages.error(request, "El nombre de la empresa es obligatorio.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                nit = request.POST.get('nit', '')
                if not nit:
                    messages.error(request, "El NIT es obligatorio.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                email_empresa = request.POST.get('email_empresa', '')
                if not email_empresa:
                    messages.error(request, "El email de la empresa es obligatorio.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                contraseña_empresa = request.POST.get('contraseña_empresa', '')
                if not contraseña_empresa:
                    messages.error(request, "La contraseña es obligatoria.")
                    return redirect('Registro')  # Redirigir a la misma página en caso de error
                
                nueva_persona.nombre = "Admin"  # Nombre por defecto para el contacto
                nueva_persona.nombre_empresa = nombre_empresa
                nueva_persona.nit = nit
                nueva_persona.email = email_empresa
                nueva_persona.contraseña = make_password(contraseña_empresa)  # Encriptar la contraseña antes de guardar
                nueva_persona.rol = 'Empresa'
            
            # Guardar la persona en la base de datos
            nueva_persona.save()
            
            # Mostrar mensaje de éxito
            messages.success(request, '¡Registro exitoso! Por favor inicia sesión.')
            
            # Redirigir a la página de inicio de sesión
            return redirect('Inicio_Sesion')
            
        except Exception as e:
            logger.error(f"Error en el registro: {str(e)}")
            messages.error(request, f'Error en el registro: {str(e)}')
            return redirect('Registro')  # Redirigir a la misma página en caso de error
    
    return render(request, 'Registro.html')

# Página principal
def home(request):
    usuario = verificar_autenticacion(request)
    return render(request, 'home.html', {'usuario': usuario})   

def Planes(request):
    usuario = verificar_autenticacion(request)
    return render(request, 'Planes.html', {'usuario': usuario})

# Función de inicio de sesión
def Inicio_Sesión(request):
    # Si el usuario ya está autenticado, redirigir a home
    if verificar_autenticacion(request):
        return redirect('home')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        contraseña = request.POST.get('contraseña')
        
        if not email or not contraseña:
            messages.error(request, "Por favor complete todos los campos.")
            return render(request, 'Inicio_Sesion.html')
        
        try:
            # Buscar usuario por email
            usuario = Persona.objects.get(email=email)
            
            # Verificar contraseña
            if check_password(contraseña, usuario.contraseña):
                # Guardar id de usuario en la sesión
                request.session['usuario_id'] = usuario.id
                
                # Establecer una duración de sesión (2 semanas)
                request.session.set_expiry(1209600)  # 2 semanas en segundos
                
                messages.success(request, f'¡Bienvenido, {usuario.nombre if usuario.nombre else usuario.nombre_empresa}!')
                
                # Redirigir a la página anterior si existe
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
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
        # Limpiar la sesión completamente
        request.session.flush()
    messages.success(request, '¡Has cerrado sesión correctamente!')
    return redirect('home')

# Vistas para la Caja Fuerte
@requiere_autenticacion
def caja_fuerte(request):
    usuario = verificar_autenticacion(request)
    
    # Obtener todos los documentos del usuario
    documentos = DocumentoCajaFuerte.objects.filter(usuario=usuario).order_by('-fecha_subida')
    
    return render(request, 'CajaFuerte.html', {
        'usuario': usuario,
        'documentos': documentos
    })

@requiere_autenticacion
def subir_documento(request):
    usuario = verificar_autenticacion(request)
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        categoria = request.POST.get('categoria')
        archivo = request.FILES.get('archivo')
        
        if nombre and archivo:
            # Crear nuevo documento
            documento = DocumentoCajaFuerte(
                usuario=usuario,
                nombre=nombre,
                descripcion=descripcion,
                categoria=categoria,
                archivo=archivo
            )
            documento.save()
            
            messages.success(request, '¡Documento subido con éxito!')
            return redirect('CajaFuerte')
        else:
            messages.error(request, 'Por favor, completa todos los campos requeridos.')
    
    return render(request, 'SubirDocumento.html', {'usuario': usuario})

@requiere_autenticacion
def ver_documento(request, documento_id):
    usuario = verificar_autenticacion(request)
    
    # Obtener el documento (solo si pertenece al usuario actual)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)
    
    # Abrir el archivo para descargar
    try:
        return FileResponse(documento.archivo, as_attachment=True, filename=documento.filename())
    except Exception as e:
        messages.error(request, f'Error al acceder al documento: {str(e)}')
        return redirect('CajaFuerte')

@requiere_autenticacion
def eliminar_documento(request, documento_id):
    usuario = verificar_autenticacion(request)
    
    # Obtener el documento (solo si pertenece al usuario actual)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)
    
    if request.method == 'POST':
        # Eliminar el archivo físico primero
        if documento.archivo:
            if os.path.isfile(documento.archivo.path):
                os.remove(documento.archivo.path)
        
        # Eliminar el registro de la base de datos
        documento.delete()
        
        messages.success(request, '¡Documento eliminado con éxito!')
        return redirect('CajaFuerte')
    
    return render(request, 'EliminarDocumento.html', {
        'usuario': usuario,
        'documento': documento
    })