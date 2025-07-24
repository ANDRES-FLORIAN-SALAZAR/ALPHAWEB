"""
Este archivo contiene las funciones que manejan las peticiones HTTP y devuelven respuestas HTTP.

Las vistas son responsables de la lógica de negocio y de interactuar con los modelos y plantillas
para generar la respuesta adecuada.
"""

import logging
from functools import wraps
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import DocumentoCajaFuerte, Persona

logger = logging.getLogger(__name__)

# ============================================================================
# DECORADORES Y UTILIDADES DE AUTENTICACIÓN
# ============================================================================

def verificar_autenticacion(request: HttpRequest) -> Persona | None:
    """
    Verifica la autenticación del usuario en la sesión.

    Args:
        request (HttpRequest): La solicitud HTTP del usuario.

    Returns:
        Persona | None: El objeto Persona si está autenticado, None en caso contrario.

    """
    if "usuario_id" in request.session:
        try:
            return Persona.objects.get(id=request.session["usuario_id"])
        except Persona.DoesNotExist:
            del request.session["usuario_id"]
    return None

def requiere_autenticacion(view_func: callable) -> callable:
    """
    Decorador que requiere autenticación para vistas específicas.

    Args:
        view_func (callable): La función de vista a decorar.

    Returns:
        callable: La función de vista decorada.

    """
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args: object, **kwargs: object) -> HttpResponse:
        usuario = verificar_autenticacion(request)
        if not usuario:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect("Aplicacion:inicio_sesion")  # Agregar el namespace aquí
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# ============================================================================
# VISTAS DE PÁGINAS PRINCIPALES
# ============================================================================

def home(request: HttpRequest) -> HttpResponse:
    """
    Vista para la página de inicio.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la página de inicio.

    """
    usuario = verificar_autenticacion(request)
    return render(request, "home.html", {"usuario": usuario})

def planes(request: HttpRequest) -> HttpResponse:
    """
    Vista para mostrar los planes disponibles.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la lista de planes.

    """
    usuario = verificar_autenticacion(request)
    return render(request, "planes.html", {"usuario": usuario})

# ============================================================================
# VISTAS DE AUTENTICACIÓN Y REGISTRO
# ============================================================================

def inicio_sesion(request: HttpRequest) -> HttpResponse:
    """
    Vista para el inicio de sesión de usuarios.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de inicio de sesión.

    """
    # Si el usuario ya está autenticado, redirigir a la página principal
    if request.user.is_authenticated:
        return redirect("Aplicacion:home")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        # Validar que se hayan proporcionado email y contraseña
        if not email or not password:
            messages.error(request, "Por favor ingrese su correo y contraseña")
            return render(request, "Inicio_Sesion.html")

        try:
            # Verificar si el usuario existe
            try:
                user = Persona.objects.get(email=email)
            except Persona.DoesNotExist:
                messages.error(request, "No existe una cuenta con este correo electrónico")
                return render(request, "Inicio_Sesion.html")

            # Autenticar al usuario
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                request.session["usuario_id"] = user.id

                # Redirigir según el tipo de usuario
                if user.is_staff or user.is_superuser:
                    return redirect("admin:index")
                return redirect("Aplicacion:home")
            messages.error(request, "Contraseña incorrecta")

        except Exception as e:
            logger.error(f"Error en inicio de sesión: {e!s}")
            messages.error(request, "Ocurrió un error al intentar iniciar sesión. Por favor intente nuevamente.")

    return render(request, "Inicio_Sesion.html")

def registro(request: HttpRequest) -> HttpResponse:
    """
    Vista de registro que maneja tanto personas naturales como empresas.

    Args:
        request (HttpRequest): La solicitud HTTP del usuario.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de registro.

    """
    if request.method == "POST":
        tipo_registro = request.POST.get("tipo_usuario")

        # Validaciones básicas
        errores = []

        # Validar que se haya seleccionado un tipo de registro
        if not tipo_registro:
            errores.append("Debe seleccionar un tipo de registro")
            messages.error(request, "Debe seleccionar un tipo de registro")

        # Validaciones específicas por tipo de registro
        if tipo_registro == "natural":
            # Datos para persona natural
            nombre = request.POST.get("nombre_completo", "").strip()
            email = request.POST.get("email_natural", "").strip().lower()
            password = request.POST.get("password1", "")
            password_confirm = request.POST.get("password2", "")
            telefono = request.POST.get("telefono_natural", "").strip()
            edad = request.POST.get("edad", "").strip()
            genero = request.POST.get("genero", "")

            # Validar campos obligatorios
            if not nombre:
                errores.append("El nombre completo es requerido")
                messages.error(request, "El nombre completo es requerido")
            if not email:
                errores.append("El correo electrónico es requerido")
                messages.error(request, "El correo electrónico es requerido")
            elif "@" not in email:
                errores.append("Ingrese un correo electrónico válido")
                messages.error(request, "Ingrese un correo electrónico válido")
            if not telefono:
                errores.append("El teléfono es requerido")
                messages.error(request, "El teléfono es requerido")
            if not password:
                errores.append("La contraseña es requerida")
                messages.error(request, "La contraseña es requerida")
            elif len(password) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres")
                messages.error(request, "La contraseña debe tener al menos 8 caracteres")
            if not edad.isdigit() or not (18 <= int(edad) <= 100):
                errores.append("La edad debe ser un número entre 18 y 100")
                messages.error(request, "La edad debe ser un número entre 18 y 100")

            # Validar que las contraseñas coincidan
            if password != password_confirm:
                errores.append("Las contraseñas no coinciden")
                messages.error(request, "Las contraseñas no coinciden")

        elif tipo_registro == "empresa":
            # Datos para empresa
            razon_social = request.POST.get("razon_social", "").strip()
            nit = request.POST.get("nit", "").strip()
            email_empresa = request.POST.get("email_empresa", "").strip().lower()
            telefono_empresa = request.POST.get("telefono_empresa", "").strip()
            direccion = request.POST.get("direccion", "").strip()
            representante_legal = request.POST.get("representante_legal", "").strip()
            sitio_web = request.POST.get("sitio_web", "").strip()
            password_empresa = request.POST.get("password_empresa", "")
            confirmar_password_empresa = request.POST.get("confirmar_password_empresa", "")

            # Obtener datos adicionales específicos de empresa
            empresa_tipo = request.POST.get("empresa_tipo", "")
            empresa_segmento = request.POST.get("empresa_segmento", "")
            empresa_tamano = request.POST.get("empresa_tamaño", "")
            empresa_num_empleados = request.POST.get("empresa_numero_empleados", "")
            empresa_pais = request.POST.get("empresa_pais", "")
            empresa_ciudad = request.POST.get("empresa_ciudad", "")
            empresa_descripcion = request.POST.get("empresa_descripcion", "")

            # Validar campos obligatorios
            if not razon_social:
                errores.append("La razón social es requerida")
                messages.error(request, "La razón social es requerida")
            if not nit:
                errores.append("El NIT es requerido")
                messages.error(request, "El NIT es requerido")
            if not email_empresa:
                errores.append("El correo electrónico de la empresa es requerido")
                messages.error(request, "El correo electrónico de la empresa es requerido")
            elif "@" not in email_empresa:
                errores.append("Ingrese un correo electrónico válido")
                messages.error(request, "Ingrese un correo electrónico válido")
            if not telefono_empresa:
                errores.append("El teléfono de la empresa es requerido")
                messages.error(request, "El teléfono de la empresa es requerido")
            if not direccion:
                errores.append("La dirección es requerida")
                messages.error(request, "La dirección es requerida")
            if not representante_legal:
                errores.append("El nombre del representante legal es requerido")
                messages.error(request, "El nombre del representante legal es requerido")
            if not password_empresa:
                errores.append("La contraseña es requerida")
                messages.error(request, "La contraseña es requerida")
            elif len(password_empresa) < 8:
                errores.append("La contraseña debe tener al menos 8 caracteres")
                messages.error(request, "La contraseña debe tener al menos 8 caracteres")

            # Validar que las contraseñas coincidan
            if password_empresa != confirmar_password_empresa:
                errores.append("Las contraseñas no coinciden")
                messages.error(request, "Las contraseñas no coinciden")

        # Si hay errores, mostrar el formulario con los errores
        if errores:
            context = {
                "tipo_usuario": tipo_registro,
                "errores": errores,
            }

            # Agregar datos según el tipo de registro para mantener los valores en el formulario
            if tipo_registro == "natural":
                context.update({
                    "nombre_completo": nombre,
                    "email": email,
                    "telefono": telefono,
                    "edad": edad,
                    "genero": genero,
                })
            elif tipo_registro == "empresa":
                context.update({
                    "razon_social": razon_social,
                    "nit": nit,
                    "email_empresa": email_empresa,
                    "telefono_empresa": telefono_empresa,
                    "direccion": direccion,
                    "representante_legal": representante_legal,
                    "sitio_web": sitio_web,
                })

            return render(request, "registro.html", context)

        # Si llegamos aquí, los datos son válidos
        try:
            if tipo_registro == "natural":
                # Verificar si el email ya existe
                if Persona.objects.filter(email=email).exists():
                    messages.error(request, "Este correo electrónico ya está registrado")
                    return render(request, "registro.html", {
                        "tipo_usuario": tipo_registro,
                        "nombre_completo": nombre,
                        "email": email,
                        "telefono": telefono,
                        "edad": edad,
                        "genero": genero,
                    })

                # Crear el diccionario de datos del usuario
                user_data = {
                    "email": email,
                    "password": password,
                    "first_name": nombre,
                    "last_name": "",
                    "telefono": telefono,
                    "edad": int(edad) if edad and edad.isdigit() else None,
                    "genero": genero,
                    "rol": "Usuario",
                    "is_active": True,
                    "es_empresa": False,
                }

                # Crear el usuario
                user = Persona.objects.create_user(**user_data)
                messages.success(request, f"¡Registro exitoso! Bienvenido/a {nombre}")

            elif tipo_registro == "empresa":
                # Verificar si el email o NIT ya existen
                if Persona.objects.filter(email=email_empresa).exists():
                    messages.error(request, "Este correo electrónico ya está registrado")
                    return render(request, "registro.html", {
                        "tipo_usuario": tipo_registro,
                        "razon_social": razon_social,
                        "nit": nit,
                        "email_empresa": email_empresa,
                        "telefono_empresa": telefono_empresa,
                        "direccion": direccion,
                        "representante_legal": representante_legal,
                        "sitio_web": sitio_web,
                    })

                if Persona.objects.filter(nit=nit).exists():
                    messages.error(request, "Este NIT ya está registrado")
                    return render(request, "registro.html", {
                        "tipo_usuario": tipo_registro,
                        "razon_social": razon_social,
                        "nit": nit,
                        "email_empresa": email_empresa,
                        "telefono_empresa": telefono_empresa,
                        "direccion": direccion,
                        "representante_legal": representante_legal,
                        "sitio_web": sitio_web,
                    })

                # Crear el diccionario de datos del usuario empresa
                user_data = {
                    "email": email_empresa,
                    "password": password_empresa,
                    "first_name": razon_social,  # Usar razón social como nombre
                    "last_name": "",
                    "telefono": telefono_empresa,
                    "rol": "Usuario",
                    "is_active": True,
                    "es_empresa": True,
                    "razon_social": razon_social,
                    "nit": nit,
                    "direccion": direccion,
                    "representante_legal": representante_legal,
                    "sitio_web": sitio_web if sitio_web else None,
                }

                # Crear el usuario empresa
                user = Persona.objects.create_user(**user_data)
                messages.success(request, f"¡Registro de empresa exitoso! Bienvenido/a {razon_social}")
            else:
                raise ValueError("Tipo de registro no válido")

            # Iniciar sesión automáticamente
            login(request, user)
            request.session["usuario_id"] = user.id

            # Redirigir a la caja fuerte después del registro
            return redirect("Aplicacion:caja_fuerte")

        except Exception as e:
            # Manejar errores específicos de la base de datos
            if "duplicate" in str(e).lower() or "ya existe" in str(e).lower():
                error_msg = "Este correo electrónico o NIT ya está registrado"
            else:
                error_msg = f"Error al crear el usuario: {e!s}"

            logger.error(f"Error en el registro: {e!s}")
            messages.error(request, error_msg)

            # Preparar el contexto para volver a mostrar el formulario
            context = {
                "tipo_usuario": tipo_registro,
                "errores": [error_msg],
            }

            if tipo_registro == "natural":
                context.update({
                    "nombre_completo": nombre,
                    "email": email,
                    "telefono": telefono,
                    "edad": edad,
                    "genero": genero,
                })
            elif tipo_registro == "empresa":
                context.update({
                    "razon_social": razon_social,
                    "nit": nit,
                    "email_empresa": email_empresa,
                    "telefono_empresa": telefono_empresa,
                    "direccion": direccion,
                    "representante_legal": representante_legal,
                    "sitio_web": sitio_web,
                })

            return render(request, "registro.html", context)

    # GET request - mostrar formulario vacío
    return render(request, "registro.html")

def cerrar_sesion(request: HttpRequest) -> HttpResponse:
    """
    Vista para cerrar sesión del usuario de forma segura.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: Redirección a la página de inicio con mensaje de confirmación.

    """
    # Verificar si el usuario está autenticado
    if request.user.is_authenticated:
        # Guardar el nombre del usuario para el mensaje
        username = request.user.get_short_name() or request.user.email

        # Cerrar la sesión de Django
        logout(request)

        # Limpiar la sesión completamente
        request.session.flush()

        # Eliminar la cookie de sesión del navegador
        if hasattr(request, "session"):
            request.session.delete()

        # Eliminar la cookie de sesión manualmente
        response = redirect("Aplicacion:home")
        response.delete_cookie("sessionid")
        response.delete_cookie("csrftoken")  # También limpiamos el token CSRF

        # Mensaje de confirmación
        messages.success(request, f"Has cerrado sesión correctamente. ¡Hasta pronto, {username}!")

        # Registrar el cierre de sesión
        logger.info(f"Usuario {username} ha cerrado sesión correctamente")

        return response

    # Si el usuario no estaba autenticado, redirigir al inicio
    return redirect("Aplicacion:home")

def contrasenas(request: HttpRequest) -> HttpResponse:
    """
    Vista para el generador de contraseñas (accesible para todos los usuarios).
    
    Mantiene el nombre original para compatibilidad con tu HTML existente.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el generador de contraseñas.

    """
    usuario = verificar_autenticacion(request)
    # Usa tu HTML existente llamado "Contrasenas.html"
    return render(request, "Contrasenas.html", {"usuario": usuario})

@requiere_autenticacion
def cambiar_contrasena(request: HttpRequest) -> HttpResponse:
    """
    Vista para cambiar la contraseña del usuario logueado.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de cambio de contraseña.

    """
    usuario = verificar_autenticacion(request)

    if request.method == "POST":
        password_actual = request.POST.get("password_actual")
        nueva_password = request.POST.get("nueva_password")
        confirmar_password = request.POST.get("confirmar_password")

        # Validaciones
        if not password_actual or not nueva_password or not confirmar_password:
            messages.error(request, "Todos los campos son requeridos.")
            return render(request, "cambiar_contrasena.html", {"usuario": usuario})

        if nueva_password != confirmar_password:
            messages.error(request, "Las nuevas contraseñas no coinciden.")
            return render(request, "cambiar_contrasena.html", {"usuario": usuario})

        if len(nueva_password) < 8:
            messages.error(request, "La nueva contraseña debe tener al menos 8 caracteres.")
            return render(request, "cambiar_contrasena.html", {"usuario": usuario})

        if not usuario.check_password(password_actual):
            messages.error(request, "La contraseña actual es incorrecta.")
            return render(request, "cambiar_contrasena.html", {"usuario": usuario})

        try:
            usuario.set_password(nueva_password)
            usuario.save()

            # Re-autenticar al usuario para mantener la sesión
            user = authenticate(request, username=usuario.email, password=nueva_password)
            if user:
                login(request, user)
                request.session["usuario_id"] = user.id

            messages.success(request, "Contraseña cambiada exitosamente.")
            logger.info(f"Usuario {usuario.email} cambió su contraseña exitosamente")
            return redirect("Aplicacion:caja_fuerte")

        except Exception as e:
            logger.error(f"Error al cambiar contraseña para usuario {usuario.email}: {e!s}")
            messages.error(request, "Ocurrió un error al cambiar la contraseña. Por favor intente nuevamente.")

    return render(request, "cambiar_contrasena.html", {"usuario": usuario})

# Función obsoleta - puedes eliminarla
def generador_contrasenas_obsoleto(request: HttpRequest) -> HttpResponse:
    """
    FUNCIÓN OBSOLETA - Usar contrasenas() para el generador y cambiar_contrasena() para cambio.
    
    Esta función se mantiene solo como referencia.
    """
    # Redirigir a la vista apropiada
    return redirect("Aplicacion:contrasenas")

def listar_empresas(request: HttpRequest) -> HttpResponse:
    """Vista para listar empresas activas."""
    empresas = Empresa.objects.filter(activa=True).select_related(
        "tipo_empresa", "segmento",
    ).prefetch_related("perfilusuario_set")

    context = {
        "empresas": empresas,
    }
    return render(request, "listar_empresas.html", context)

# ============================================================================
# VISTAS DE CAJA FUERTE

def custom_404(request: HttpRequest, exception=None) -> HttpResponse:
    """
    Maneja errores 404 (página no encontrada) mostrando una página personalizada

    Args:
        request (HttpRequest): La solicitud HTTP.
        exception: La excepción que causó el error 404.

    Returns:
        HttpResponse: La página de error 404 personalizada.

    """
    # Aseguramos que la URL sea '/404/' para que se aplique el estilo
    request.path = "/404/"

    # Agregamos el contexto necesario para que la plantilla funcione
    context = {
        "request": request,
    }

    return render(request, "404.html", context=context, status=404)

# VISTAS DE CAJA FUERTE
# ============================================================================

@requiere_autenticacion
def caja_fuerte(request: HttpRequest) -> HttpResponse:
    """
    Vista para la caja fuerte del usuario.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con la caja fuerte del usuario.

    """
    usuario = verificar_autenticacion(request)
    documentos = DocumentoCajaFuerte.objects.filter(usuario=usuario).order_by("-fecha_subida")
    return render(request, "caja_fuerte.html", {
        "usuario": usuario,
        "documentos": documentos,
    })

@requiere_autenticacion
def subir_documento(request: HttpRequest) -> HttpResponse:
    """
    Vista para subir documentos a la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP después de intentar subir el documento.

    """
    usuario = verificar_autenticacion(request)

    if not usuario:
        messages.error(request, "Debes iniciar sesión para subir documentos.")
        return redirect("inicio_sesion")

    if request.method == "POST":
        try:
            nombre = request.POST.get("nombre", "").strip()
            archivo = request.FILES.get("archivo")
            max_file_size = 5242880  # 5MB

            if not nombre or not archivo:
                messages.error(request, "Debe proporcionar un nombre y seleccionar un archivo.")
                return redirect("Aplicacion:subir_documento")

            if archivo.size > max_file_size:
                messages.error(request, "El archivo es demasiado grande. El tamaño máximo permitido es 5MB.")
                return redirect("Aplicacion:subir_documento")

            # Crear el documento
            documento = DocumentoCajaFuerte(
                usuario=usuario,
                nombre=nombre,
                descripcion=request.POST.get("descripcion", ""),
                categoria=request.POST.get("categoria", "Otros"),
                archivo=archivo,
            )
            documento.save()

            # Verificar si el archivo se guardó correctamente
            class UploadError(Exception):
                def __init__(self) -> None:
                    super().__init__("El archivo no se guardó correctamente en el servidor")

            def raise_upload_error() -> None:
                """Lanza un error si el archivo no se guardó correctamente."""
                raise UploadError  # noqa: TRY301

            if not documento.archivo.storage.exists(documento.archivo.name):
                raise_upload_error()

            messages.success(request, "¡Documento subido con éxito!")
            logger.info("Documento subido exitosamente: %s - %s", documento.id, documento.nombre)
            return redirect("Aplicacion:caja_fuerte")

        except Exception as e:
            logger.exception("Error al subir documento", extra={"user_id": getattr(usuario, "id", None)})
            messages.error(request, f"Error al subir el documento: {e!s}")
            return redirect("Aplicacion:subir_documento")

    return render(request, "subir_documento.html", {"usuario": usuario})

@requiere_autenticacion
def ver_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    """
    Vista para ver un documento en la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.
        documento_id (int): El ID del documento a ver.

    Returns:
        HttpResponse: El archivo solicitado o redirección en caso de error.

    """
    try:
        usuario = verificar_autenticacion(request)
        documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)
        archivo = documento.archivo

        # Verificar si el archivo existe
        if not archivo.storage.exists(archivo.name):
            logger.error("Archivo no encontrado: %s", archivo.name)
            messages.error(request, "El archivo solicitado no existe en el servidor.")
            return redirect("Aplicacion:caja_fuerte")

        # Obtener el nombre del archivo
        nombre_archivo = archivo.name.split("/")[-1]

        # Determinar el tipo de contenido basado en la extensión
        extension = nombre_archivo.split(".")[-1].lower()
        content_type = {
            "pdf": "application/pdf",
            "doc": "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "xls": "application/vnd.ms-excel",
            "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "txt": "text/plain",
        }.get(extension, "application/octet-stream")

        # Crear la respuesta
        response = FileResponse(archivo, as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{nombre_archivo}"'
        response["Content-Type"] = content_type

        return response

    except Exception:
        logger.exception("Error al acceder al documento %d", documento_id)
        messages.error(request, "Error al acceder al documento. Por favor, inténtalo de nuevo.")
        return redirect("Aplicacion:caja_fuerte")
@requiere_autenticacion
def eliminar_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    """
    Elimina un documento de la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.
        documento_id (int): El ID del documento a eliminar.

    Returns:
        HttpResponse: Redirección después de eliminar o mostrar confirmación.

    """
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    if request.method == "POST":
        try:
            if documento.archivo and Path(documento.archivo.path).is_file():
                Path(documento.archivo.path).unlink()
            documento.delete()
            messages.success(request, "Documento eliminado correctamente.")
            return redirect("Aplicacion:caja_fuerte")
        except Exception:
            logger.exception("Error al eliminar el documento: %s", documento.id)
            messages.error(request, "Error al eliminar el documento.")
            return redirect("Aplicacion:caja_fuerte")

    return render(request, "eliminar_documento.html", {
        "documento": documento,
    })

@require_http_methods(["GET"])
def api_tipos_empresa(request: HttpRequest) -> JsonResponse:
    """
    Devuelve tipos de empresa.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        JsonResponse: Lista de tipos de empresa en formato JSON.

    """
    # Referenciar explícitamente el argumento request para evitar advertencias de argumento no utilizado
    _ = request
    tipos = TipoEmpresa.objects.filter(
        activo=True,
    ).values("id", "nombre", "descripcion")

    return JsonResponse(list(tipos), safe=False)

@require_http_methods(["GET"])
def api_empresa_detalle(request: HttpRequest, empresa_id: int) -> JsonResponse:
    """
    Devuelve detalles de una empresa.

    Args:
        request (HttpRequest): La solicitud HTTP.
        empresa_id (int): ID de la empresa.

    Returns:
        JsonResponse: Detalles de la empresa en formato JSON.

    """
    # Usar el argumento request para evitar advertencias de argumento no utilizado
    logger.debug("Solicitud recibida para detalles de empresa. Método: %s, Usuario: %s", request.method, getattr(request, "user", None))
    try:
        empresa = Empresa.objects.select_related("tipo_empresa", "segmento").get(
            id=empresa_id, activa=True,
        )
        data = {
            "id": empresa.id,
            "nombre": empresa.nombre,
            "nit": empresa.nit,
            "razon_social": empresa.razon_social,
            "tipo_empresa": empresa.tipo_empresa.nombre,
            "segmento": empresa.segmento.nombre,
            "tamaño": empresa.get_tamaño_display(),
            "email": empresa.email,
            "telefono": empresa.telefono,
            "ciudad": empresa.ciudad,
            "pais": empresa.pais,
            "numero_empleados": empresa.numero_empleados,
            "requiere_2fa": empresa.requiere_autenticacion_2fa,
            "politica_estricta": empresa.politica_contraseñas_estricta,
        }
        return JsonResponse(data)
    except Empresa.DoesNotExist:
        return JsonResponse({"error": "Empresa no encontrada"}, status=404)

def crear_datos_iniciales_empresa() -> None:
    """Crea datos iniciales de tipos y segmentos de empresa."""
    # Crear tipos de empresa si no existen
    tipos_empresa = [
        {"nombre": "Sociedad de Responsabilidad Limitada", "descripcion": "Empresa constituida como SRL"},
        {"nombre": "Empresa Unipersonal", "descripcion": "Empresa constituida por una sola persona"},
        {"nombre": "Sociedad por Acciones Simplificada", "descripcion": "Empresa constituida como SAS"},
        {"nombre": "Cooperativa", "descripcion": "Organización cooperativa"},
        {"nombre": "Fundación", "descripcion": "Organización sin ánimo de lucro"},
    ]

    for tipo_data in tipos_empresa:
        TipoEmpresa.objects.get_or_create(
            nombre=tipo_data["nombre"],
            defaults={"descripcion": tipo_data["descripcion"]},
        )

    # Crear segmentos de empresa si no existen
    segmentos_empresa = [
        {"nombre": "Tecnología", "descripcion": "Empresas del sector tecnológico y software"},
        {"nombre": "Financiero", "descripcion": "Bancos, seguros y servicios financieros"},
        {"nombre": "Salud", "descripcion": "Hospitales, clínicas y servicios de salud"},
        {"nombre": "Educación", "descripcion": "Instituciones educativas y centros de formación"},
        {"nombre": "Manufactura", "descripcion": "Empresas de producción y manufactura"},
        {"nombre": "Comercio", "descripcion": "Empresas de comercio y retail"},
        {"nombre": "Servicios", "descripcion": "Empresas de servicios profesionales"},
        {"nombre": "Construcción", "descripcion": "Empresas del sector construcción y arquitectura"},
        {"nombre": "Alimentario", "descripcion": "Empresas del sector alimentario y bebidas"},
        {"nombre": "Transporte", "descripcion": "Empresas de transporte y logística"},
        {"nombre": "Energía", "descripcion": "Empresas del sector energético"},
        {"nombre": "Telecomunicaciones", "descripcion": "Empresas de telecomunicaciones y comunicaciones"},
    ]

    for segmento_data in segmentos_empresa:
        SegmentoEmpresa.objects.get_or_create(
            nombre=segmento_data["nombre"],
            defaults={"descripcion": segmento_data["descripcion"]},
        )
