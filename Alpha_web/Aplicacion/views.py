import logging
import os
from functools import wraps

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
    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args: int, **kwargs: int) -> HttpResponse:
        usuario = verificar_autenticacion(request)
        if not usuario:
            messages.error(request, "Debes iniciar sesión para acceder a esta página.")
            return redirect("Inicio_Sesion")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def Registro(request: HttpRequest) -> HttpResponse:
    if verificar_autenticacion(request):
        return redirect("home")

    if request.method == "POST":
        try:
            return registro_persona_natural(request)
        except Exception as e:
            logger.error(f"Error en registro: {e!s}")
            messages.error(request, "Error durante el registro. Intenta nuevamente.")
            return redirect("registro")

    return render(request, "Registro.html")

def registro_persona_natural(request: HttpRequest) -> HttpResponse:
    nombre_completo = request.POST.get("nombre_completo", "").strip()
    email = request.POST.get("email", "").strip()
    contrasena = request.POST.get("password", "").strip()

    if not nombre_completo:
        messages.error(request, "El nombre completo es obligatorio.")
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

    partes_nombre = nombre_completo.split(" ", 1)
    nombre = partes_nombre[0]
    apellido = partes_nombre[1] if len(partes_nombre) > 1 else ""

    nueva_persona = Persona(
        nombre=nombre,
        apellido=apellido,
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
    return redirect("Inicio_Sesion")

def home(request: HttpRequest) -> HttpResponse:

    usuario = verificar_autenticacion(request)
    return render(request, "home.html", {"usuario": usuario})

def Planes(request: HttpRequest) -> HttpResponse:
    usuario = verificar_autenticacion(request)
    return render(request, "Planes.html", {"usuario": usuario})

def Inicio_Sesion(request: HttpRequest) -> HttpResponse:
    if verificar_autenticacion(request):
        return redirect("Planes")

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
                return redirect("Planes")
            messages.error(request, "Contraseña incorrecta.")
        except Persona.DoesNotExist:
            messages.error(request, "No existe un usuario con ese email.")

    return render(request, "Inicio_Sesion.html")

def Contrasenas(request: HttpRequest) -> HttpResponse:
    usuario = verificar_autenticacion(request)
    return render(request, "Contrasenas.html", {"usuario": usuario})

def cerrar_sesion(request: HttpRequest) -> HttpResponse:
    if "usuario_id" in request.session:
        del request.session["usuario_id"]
        request.session.flush()
    messages.success(request, "¡Has cerrado sesión correctamente!")
    return redirect("home")

@requiere_autenticacion
def caja_fuerte(request: HttpRequest) -> HttpResponse:
    usuario = verificar_autenticacion(request)
    documentos = DocumentoCajaFuerte.objects.filter(usuario=usuario).order_by("-fecha_subida")
    return render(request, "CajaFuerte.html", {
        "usuario": usuario,
        "documentos": documentos,
    })

@requiere_autenticacion
def subir_documento(request: HttpRequest) -> HttpResponse:
    usuario = verificar_autenticacion(request)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        archivo = request.FILES.get("archivo")

        if not nombre or not archivo:
            messages.error(request, "Nombre y archivo son campos requeridos.")
            return redirect("SubirDocumento")

        try:
            DocumentoCajaFuerte.objects.create(
                usuario=usuario,
                nombre=nombre,
                descripcion=request.POST.get("descripcion", ""),
                categoria=request.POST.get("categoria", "Otros"),
                archivo=archivo,
            )
            messages.success(request, "¡Documento subido con éxito!")
            return redirect("SubirDocumento")
        except Exception as e:
            logger.error(f"Error al subir documento: {e!s}")
            messages.error(request, "Error al subir el documento. Intente nuevamente.")
            return redirect("SubirDocumento")

    return render(request, "SubirDocumento.html")

@requiere_autenticacion
def ver_documento(request: HttpRequest, documento_id: int) -> HttpResponse:
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    try:
        return FileResponse(
            open(documento.archivo.path, "rb"),
            as_attachment=True,
            filename=os.path.basename(documento.archivo.name),
        )
    except Exception as e:
        logger.error(f"Error al acceder al documento {documento_id}: {e!s}")
        messages.error(request, "Error al acceder al documento.")
        return redirect("caja_fuerte")

@requiere_autenticacion
def eliminar_documento(request: HttpRequest, documento_id: int):
    usuario = verificar_autenticacion(request)
    documento = get_object_or_404(DocumentoCajaFuerte, id=documento_id, usuario=usuario)

    if request.method == "POST":
        try:
            if documento.archivo and os.path.isfile(documento.archivo.path):
                os.remove(documento.archivo.path)
            documento.delete()
            messages.success(request, "Documento eliminado correctamente.")
        except Exception as e:
            logger.exception(f"Error al eliminar documento {documento_id}: {e!s}")
            messages.error(request, "Error al eliminar el documento.")

        return redirect("CajaFuerte")

    return render(request, "EliminarDocumento.html", {
        "documento": documento,
    })
