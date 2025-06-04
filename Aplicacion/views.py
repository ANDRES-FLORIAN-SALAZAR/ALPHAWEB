"""
"este archivo contiene las vistas de la aplicacion.

las cuales son funciones que manejan las peticiones HTTP y devuelven respuestas HTTP.
"""
import logging
from functools import wraps
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import DocumentoCajaFuerte, Persona

""" en este archivo se encuentran las vistas de la aplicacion

las cuales son funciones que manejan las peticiones HTTP y devuelven respuestas HTTP.

Las vistas son responsables de la logica de negocio

y de interactuar con los modelos y plantillas para generar la respuesta adecuada. """

logger = logging.getLogger(__name__)

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
    Requiere autenticación para vistas específicas.

    Args:
        view_func (callable): La función de vista a decorar.

    Returns:
        callable: La función de vista decorada.

    """

    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args: int, **kwargs: int) -> HttpResponse:
        usuario = verificar_autenticacion(request)
        if not usuario:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect("Inicio_Sesion")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def registro(request: HttpRequest) -> HttpResponse:
    """
    Módulo de vistas de la aplicación.

    Contiene las funciones que manejan las solicitudes HTTP y la lógica de negocio

    relacionada con la autenticación, registro, y otras funcionalidades.
    """
    if verificar_autenticacion(request):
        return redirect("Planes")

    if request.method == "POST":
        try:
            return registro_persona_natural(request)
        except Exception:
            logger.exception("Error en registro: %s")
            raise

    return render(request, "registro.html")

def registro_persona_natural(request: HttpRequest) -> HttpResponse:
    """
    Registra una nueva persona natural.

    Args:
        request (HttpRequest): La solicitud HTTP del usuario.

    Returns:
        HttpResponse: La respuesta HTTP después de intentar registrar a la persona.

    """
    nombre = request.POST.get("nombre", "").strip()
    apellido = request.POST.get("apellido", "").strip()
    email = request.POST.get("email", "").strip()
    contrasena = request.POST.get("contrasena", "").strip()
    confirmar_contrasena = request.POST.get("confirmar_contrasena", "").strip()

    if not nombre:
        messages.error(request, "El nombre es obligatorio.")
        return redirect("registro")
    # El apellido puede ser opcional. Si es obligatorio, descomenta las siguientes líneas:
    # if not apellido:
    #     messages.error(request, "El apellido es obligatorio.")
    #     return redirect("registro")

    if not contrasena:
        messages.error(request, "La contraseña es obligatoria.")
        return redirect("registro")

    if contrasena != confirmar_contrasena:
        messages.error(request, "Las contraseñas no coinciden.")
        return redirect("registro")

    if not email:
        messages.error(request, "El email es obligatorio.")
        return redirect("registro")
    if not contrasena:
        messages.error(request, "La contrasena es obligatoria.")
        return redirect("registro")

    if Persona.objects.filter(email=email).exists():
        messages.error(request, "El email ya está registrado.")
        return redirect("registro")

    # Ya no se divide nombre_completo, se usan nombre y apellido directamente del formulario.

    nueva_persona = Persona(
        nombre=nombre, # Directo del formulario
        apellido=apellido, # Directo del formulario
        email=email,
        contrasena=make_password(contrasena),
        telefono=request.POST.get("celular", "").strip(),
        genero=request.POST.get("genero", "").strip(),
        rol="Usuario",
    )

    if edad := request.POST.get("edad", "").strip():
        try:
            nueva_persona.edad = int(edad)
        except ValueError:
            messages.error(request, "La edad debe ser un número válido.")
            return redirect("registro")

    nueva_persona.save()
    messages.success(request, "¡Registro exitoso! Por favor inicia sesión.")
    return redirect("inicio_sesion")

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

def inicio_sesion(request: HttpRequest) -> HttpResponse:
    """
    Vista para el inicio de sesión.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: La respuesta HTTP con el formulario de inicio de sesión.

    """
    if verificar_autenticacion(request):

        return redirect("planes")

    if request.method == "POST":
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")

        if not email or not contrasena:
            messages.error(request, "Por favor complete todos los campos.")
            return render(request, "Inicio_Sesion.html")

        try:
            usuario = Persona.objects.get(email=email)
            if check_password(contrasena, usuario.contrasena):
                request.session["usuario_id"] = usuario.id
                request.session.set_expiry(1209600)

                messages.success(request, f"¡Bienvenido, {usuario.nombre}!")
                return redirect("planes")
            messages.error(request, "Contraseña incorrecta.")
        except Persona.DoesNotExist:
            messages.error(request, "No existe un usuario con ese email.")

    return render(request, "Inicio_Sesion.html")

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
    return redirect("home")

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

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        archivo = request.FILES.get("archivo")

        if not nombre or not archivo:
            messages.error(request, "Nombre y archivo son campos requeridos.")
            return redirect("subir_documento")

        try:
            DocumentoCajaFuerte.objects.create(
                usuario=usuario,
                nombre=nombre,
                descripcion=request.POST.get("descripcion", ""),
                categoria=request.POST.get("categoria", "Otros"),
                archivo=archivo,
            )
            messages.success(request, "¡Documento subido con éxito!")
            return redirect("caja_fuerte")
        except Exception:
            logger.exception("Error al subir documento", extra={"user_id": usuario.nombre})
            messages.error(request, "Error al subir el documento. Intente nuevamente.")
            return redirect("subir_documento")

    return render(request, "subir_documento.html", {"usuario": usuario})

@requiere_autenticacion
def ver_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    """
    Vista para ver un documento en la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.
        documento_id (int): El ID del documento a ver.

    Returns:
        HttpResponse: La respuesta HTTP con el documento solicitado.

    """
    usuario = verificar_autenticacion(request)
    if not usuario:
        messages.error(request, "Debes iniciar sesión para acceder a esta página.")
        return redirect("Inicio_Sesion")
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    try:
        with Path.open(documento.archivo.path, "rb") as file_handle:
            response = FileResponse(
                file_handle,
                as_attachment=True,
            )
            response["Content-Disposition"] = f'attachment; filename="{documento.archivo.name}"'
            return response
    except Exception:
        logger.exception("Error al acceder al documento: %s", documento.id)
        messages.error(request, "Error al acceder al documento.")
    return redirect("caja_fuerte")


def custom_404_view(request: HttpRequest, exception) -> HttpResponse:
    """
    Vista personalizada para errores 404.
    Renderiza la plantilla 404.html.
    """
    return render(request, "404.html", status=404)


@requiere_autenticacion

def descargar_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    """
    Descarga un documento de la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.
        documento_id (int): El ID del documento a descargar.

    Returns:
        HttpResponse: La respuesta HTTP con el archivo descargado.

    """
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    try:
        with Path.open(documento.archivo.path, "rb") as file_handle:
            response = FileResponse(
                file_handle,
                as_attachment=True,
            )
            response["Content-Disposition"] = f'attachment; filename="{documento.archivo.name}"'
            return response
    except Exception as e:
        logger.exception("Error detallado al intentar descargar el documento ID %s:", documento.id)
        # messages.error(request, "Error al descargar el documento.") # Mensaje genérico temporalmente desactivado
        # return redirect("caja_fuerte") # Redirección temporalmente desactivada
        raise e # Re-lanzar la excepción para ver el error completo en el navegador
    
@requiere_autenticacion
def eliminar_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    """
    Elimina un documento de la caja fuerte.

    Args:
        request (HttpRequest): La solicitud HTTP.
        documento_id (int): El ID del documento a eliminar.

    Returns:
        HttpResponse: La respuesta HTTP después de intentar eliminar el documento.

    """
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    if request.method == "POST":
        try:
            if documento.archivo and Path(documento.archivo.path).is_file():
                Path(documento.archivo.path).unlink()
            documento.delete()
            messages.success(request, "Documento eliminado correctamente.")
        except Exception:
            logger.exception("Error al eliminar el documento: %s", documento.id)
            messages.error(request, "Error al eliminar el documento.")

        return redirect("caja_fuerte")

    return render(request, "eliminar_documento.html", {
        "documento": documento,
    })
