"""
Este archivo contiene las funciones que manejan las peticiones HTTP y devuelven respuestas HTTP.

Las vistas son responsables de la lógica de negocio y de interactuar con los modelos y plantillas
para generar la respuesta adecuada.
"""

import logging
from functools import wraps
from pathlib import Path

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import (
    DocumentoCajaFuerte,
    Empresa,
    PerfilUsuario,
    Persona,
    SegmentoEmpresa,
    TipoEmpresa,
)

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
            return redirect("Inicio_Sesion")
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
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: La respuesta HTTP con la página de inicio de sesión o redirección.

    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Validar campos requeridos
        if not email:
            messages.error(request, "El email es requerido.")
            return render(request, "Inicio_Sesion.html")
        if not password:
            messages.error(request, "La contraseña es requerida.")
            return render(request, "Inicio_Sesion.html")

        try:
            # Intentar autenticar al usuario usando el backend de autenticación
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                request.session["usuario_id"] = user.id
                messages.success(request, "¡Inicio de sesión exitoso!")
                return redirect("home")
            messages.error(request, "Email o contraseña incorrectos.")
            return render(request, "Inicio_Sesion.html")
        except Exception:
            logger.exception("Error inesperado en inicio de sesión")
            messages.error(request, "Error inesperado. Por favor, intenta nuevamente.")
            return render(request, "Inicio_Sesion.html")

    return render(request, "Inicio_Sesion.html")

def registro(request: HttpRequest) -> HttpResponse:
    """
    Vista de registro que maneja tanto personas naturales como usuarios con empresa.

    Args:
        request (HttpRequest): La solicitud HTTP del usuario.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de registro.

    """
    if verificar_autenticacion(request):
        return redirect("Planes")

    if request.method == "POST":
        tipo_usuario = request.POST.get("tipo_usuario")
        def raise_value_error(msg: str) -> None:
            raise ValueError(msg)
        try:
            if tipo_usuario == "natural":
                # Validaciones para persona natural
                nombre_completo = request.POST.get("nombre_completo", "").strip()
                email = request.POST.get("email", "").strip()
                password1 = request.POST.get("password1", "").strip()
                password2 = request.POST.get("password2", "").strip()
                edad = request.POST.get("edad", "").strip()
                telefono = request.POST.get("telefono", "").strip()
                genero = request.POST.get("genero", "").strip()

                if not nombre_completo or not email or not password1 or not password2:
                    raise_value_error("Todos los campos son obligatorios")

                if password1 != password2:
                    raise_value_error("Las contraseñas no coinciden")

                if Persona.objects.filter(email=email).exists():
                    raise_value_error("El correo electrónico ya está registrado")

                nueva_persona = Persona.objects.create_user(
                    email=email,
                    password=password1,
                    first_name=nombre_completo,
                    edad=edad,
                    telefono=telefono,
                    genero=genero,
                )

                user = authenticate(request, email=email, password=password1)
                if user is not None:
                    login(request, user)
                    request.session["usuario_id"] = nueva_persona.id
                    messages.success(request, "¡Registro exitoso! Has iniciado sesión.")
                    return redirect("Planes")

            elif tipo_usuario == "empresa":
                # Validaciones para empresa
                empresa_nombre = request.POST.get("empresa_nombre", "").strip()
                empresa_nit = request.POST.get("empresa_nit", "").strip()
                empresa_razon_social = request.POST.get("empresa_razon_social", "").strip()
                email = request.POST.get("email", "").strip()
                telefono = request.POST.get("telefono", "").strip()
                empresa_pais = request.POST.get("empresa_pais", "").strip()
                empresa_ciudad = request.POST.get("empresa_ciudad", "").strip()
                empresa_direccion = request.POST.get("empresa_direccion", "").strip()
                empresa_sitio_web = request.POST.get("empresa_sitio_web", "").strip()
                empresa_descripcion = request.POST.get("empresa_descripcion", "").strip()
                empresa_numero_empleados = request.POST.get("empresa_numero_empleados", "").strip()
                empresa_requiere_2fa = request.POST.get("empresa_requiere_2fa") == "on"
                empresa_politica_estricta = request.POST.get("empresa_politica_estricta") == "on"

                if not empresa_nombre or not empresa_nit or not empresa_razon_social or not email:
                    raise_value_error("Todos los campos obligatorios deben ser completados")

                if Persona.objects.filter(email=email).exists():
                    raise_value_error("El correo electrónico ya está registrado")

                nueva_persona = Persona.objects.create_user(
                    email=email,
                    password=request.POST.get("password1", ""),
                    first_name=empresa_nombre,
                )

                PerfilUsuario.objects.create(
                    usuario=nueva_persona,
                    empresa_nombre=empresa_nombre,
                    empresa_nit=empresa_nit,
                    empresa_razon_social=empresa_razon_social,
                    empresa_pais=empresa_pais,
                    empresa_ciudad=empresa_ciudad,
                    empresa_direccion=empresa_direccion,
                    empresa_sitio_web=empresa_sitio_web,
                    empresa_descripcion=empresa_descripcion,
                    empresa_numero_empleados=empresa_numero_empleados,
                    empresa_requiere_2fa=empresa_requiere_2fa,
                    empresa_politica_estricta=empresa_politica_estricta,
                )

                user = authenticate(request, email=email, password=request.POST.get("password1", ""))
                if user is not None:
                    login(request, user)
                    request.session["usuario_id"] = nueva_persona.id
                    messages.success(request, "¡Registro exitoso! Has iniciado sesión.")
                    return redirect("Planes")

            else:
                raise_value_error("Tipo de usuario no válido")

        except ValueError as e:
            messages.error(request, str(e))
            return render(request, "registro.html", {
                **get_context_data(),
                "tipo_usuario": tipo_usuario,
                **request.POST.dict(),
            })
    # Si no es POST o hay error, renderizar el formulario vacío
    return render(request, "registro.html", get_context_data())
def get_context_data() -> dict:
    """
    Obtiene el contexto común para las vistas de registro.

    Returns:
        dict: Un diccionario con los datos del contexto.

    """
    return {
        "segmentos": SegmentoEmpresa.objects.all(),
        "tipos_empresa": TipoEmpresa.objects.all(),
        "paises": [
            ("AR", "Argentina"),
            ("BO", "Bolivia"),
            ("BR", "Brasil"),
            ("CL", "Chile"),
            ("CO", "Colombia"),
            ("EC", "Ecuador"),
            ("MX", "México"),
            ("PE", "Perú"),
            ("PY", "Paraguay"),
            ("UY", "Uruguay"),
            ("US", "Estados Unidos"),
            ("VE", "Venezuela"),
        ],
    }

# Esta función no es necesaria porque la lógica ya está en la vista 'registro'

def cerrar_sesion(request: HttpRequest) -> HttpResponse:
    """
    Vista para cerrar sesión del usuario.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP después de cerrar sesión.

    """
    if "usuario_id" in request.session:
        request.session.flush()
    messages.success(request, "¡Has cerrado sesión correctamente!")
    return redirect("Aplicacion:home")

def contrasenas(request: HttpRequest) -> HttpResponse:
    """
    Vista para cambiar la contraseña del usuario.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP después de intentar cambiar la contraseña.

    """
    usuario = verificar_autenticacion(request)
    return render(request, "Contrasenas.html", {"usuario": usuario})

# ============================================================================
# VISTAS DE EMPRESAS
# ============================================================================

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
        return redirect("Inicio_Sesion")

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
