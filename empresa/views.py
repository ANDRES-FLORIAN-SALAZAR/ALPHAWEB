"""vistas.py - Manejo de vistas para la sección de empresas en ALPHAWEB."""
import logging
import os
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

User = get_user_model()
logger = logging.getLogger(__name__)

def procesar_registro_empresa(request: HttpRequest, user: User) -> HttpResponse:
    """Procesar el registro específico de empresa."""
    try:
        # Obtener datos del formulario
        empresa_datos = {
            "nombre": request.POST.get("empresa_nombre"),
            "nit": request.POST.get("empresa_nit"),
            "razon_social": request.POST.get("empresa_razon_social"),
            "tipo": request.POST.get("empresa_tipo"),
            "segmento": request.POST.get("empresa_segmento"),
            "tamaño": request.POST.get("empresa_tamaño"),
            "telefono": request.POST.get("telefono"),
            "email": request.POST.get("email"),
            "pais": request.POST.get("empresa_pais"),
            "ciudad": request.POST.get("empresa_ciudad"),
            "direccion": request.POST.get("empresa_direccion"),
            "sitio_web": request.POST.get("empresa_sitio_web"),
            "descripcion": request.POST.get("empresa_descripcion"),
            "numero_empleados": request.POST.get("empresa_numero_empleados"),
            "requiere_2fa": request.POST.get("empresa_requiere_2fa") == "on",
            "politica_estricta": request.POST.get("empresa_politica_estricta") == "on",
        }

        # Validar campos obligatorios
        campos_obligatorios = ["nombre", "nit", "razon_social", "tipo", "segmento", "tamaño", "telefono", "pais", "ciudad", "direccion", "numero_empleados"]
        campos_faltantes = [campo for campo in campos_obligatorios if not empresa_datos.get(campo)]

        if campos_faltantes:
            messages.error(request, f'Campos obligatorios faltantes: {", ".join(campos_faltantes)}')
            user.delete()
            return render(request, "registro.html", {"paises": [("CO", "Colombia")]})

        # Configurar nombre del usuario
        user.first_name = empresa_datos["nombre"]
        user.last_name = "Empresa"
        user.save()

        # Crear perfil básico en Aplicacion
        from Aplicacion.models import PerfilUsuario
        PerfilUsuario.objects.create(
            usuario=user,
            tipo_usuario="empresa",
            telefono=empresa_datos["telefono"],
        )

        # Obtener tipo de empresa
        tipo_empresa = TipoEmpresa.objects.get(id=int(empresa_datos["tipo"]))

        # Crear perfil específico de empresa
        PerfilEmpresa.objects.create(
            usuario=user,
            nombre=empresa_datos["nombre"],
            nit=empresa_datos["nit"],
            razon_social=empresa_datos["razon_social"],
            tipo=tipo_empresa,
            segmento=empresa_datos["segmento"],
            tamaño=empresa_datos["tamaño"],
            pais=empresa_datos["pais"],
            ciudad=empresa_datos["ciudad"],
            direccion=empresa_datos["direccion"],
            sitio_web=empresa_datos["sitio_web"] or "",
            descripcion=empresa_datos["descripcion"] or "",
            numero_empleados=int(empresa_datos["numero_empleados"]),
            telefono=empresa_datos["telefono"],
            email=empresa_datos["email"],
            requiere_2fa=empresa_datos["requiere_2fa"],
            politica_estricta=empresa_datos["politica_estricta"],
        )

        messages.success(request, f'¡Bienvenido {empresa_datos["nombre"]}! Tu cuenta empresarial ha sido creada exitosamente.')

        # Login automático
        user = authenticate(username=user.email, password=request.POST.get("password1"))
        if user:
            login(request, user)
            return redirect("empresa:dashboard")  # Redirigir al dashboard de empresa

    except Exception as e:
        logger.error(f"Error creando perfil empresa: {e!s}")
        user.delete()
        messages.error(request, f"Error al crear el perfil empresarial: {e!s}")

    return render(request, "registro.html", {"paises": [("CO", "Colombia")]})

def registro(request):
    """Vista para el registro de nuevas empresas"""
    if request.method == "POST":
        # Procesar el formulario de registro
        form_data = {
            "email": request.POST.get("email"),
            "password1": request.POST.get("password1"),
            "password2": request.POST.get("password2"),
            # Agrega aquí los demás campos del formulario
        }

        # Validar contraseñas
        if form_data["password1"] != form_data["password2"]:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "empresa/registro.html", {"form_data": form_data})

        # Crear el usuario
        try:
            user = User.objects.create_user(
                email=form_data["email"],
                password=form_data["password1"],
                is_company=True,  # Asegúrate de que tu modelo User tenga este campo
            )

            # Procesar el registro de la empresa
            return procesar_registro_empresa(request, user)

        except Exception as e:
            messages.error(request, f"Error al crear el usuario: {e!s}")
            return render(request, "empresa/registro.html", {"form_data": form_data})

    # Si es GET, mostrar el formulario de registro
    return render(request, "empresa/registro.html")

def inicio_sesion(request):
    """Vista para el inicio de sesión de empresas"""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_company:  # Asegurarse de que sea una cuenta de empresa
            login(request, user)
            next_url = request.GET.get("next", "empresa:dashboard")
            return redirect(next_url)
        messages.error(request, "Credenciales inválidas o cuenta no es de empresa")
        return render(request, "empresa/inicio_sesion.html", {"email": email})

    # Si es GET, mostrar el formulario de inicio de sesión
    return render(request, "empresa/inicio_sesion.html")

def home(request):
    """Vista principal de la sección de empresas"""
    return render(request, "empresa/home.html")

@login_required
def planes(request):
    """Vista para mostrar los planes de suscripción disponibles"""
    # Verificar si el usuario es una empresa
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        messages.error(request, "Acceso restringido a empresas")
        return redirect("empresa:inicio_sesion")

    # Aquí puedes agregar la lógica para obtener los planes de tu base de datos
    # Por ahora, usaremos datos de ejemplo
    planes = [
        {
            "nombre": "Básico",
            "precio": "29.99",
            "caracteristicas": ["Característica 1", "Característica 2", "Característica 3"],
            "recomendado": False,
        },
        {
            "nombre": "Profesional",
            "precio": "59.99",
            "caracteristicas": ["Todo en Básico", "Característica 4", "Característica 5"],
            "recomendado": True,
        },
        {
            "nombre": "Empresarial",
            "precio": "99.99",
            "caracteristicas": ["Todo en Profesional", "Característica 6", "Soporte prioritario"],
            "recomendado": False,
        },
    ]

    return render(request, "empresa/planes.html", {"planes": planes})

@login_required
def caja_fuerte(request):
    """Vista para la caja fuerte de la empresa"""
    # Verificar si el usuario es una empresa
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        messages.error(request, "Acceso restringido a empresas")
        return redirect("empresa:inicio_sesion")

    try:
        # Obtener el perfil de la empresa
        perfil_empresa = PerfilEmpresa.objects.get(usuario=request.user)

        # Aquí puedes agregar la lógica para obtener los elementos de la caja fuerte
        # Por ahora, devolvemos un contexto vacío
        context = {
            "perfil": perfil_empresa,
            "elementos": [],  # Aquí irían los elementos de la caja fuerte
        }

        return render(request, "empresa/caja_fuerte.html", context)

    except PerfilEmpresa.DoesNotExist:
        messages.error(request, "No se encontró el perfil de la empresa")
        return redirect("empresa:perfil")

@login_required
def contrasenas(request):
    """Vista para gestionar contraseñas en la caja fuerte"""
    # Verificar si el usuario es una empresa
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        messages.error(request, "Acceso restringido a empresas")
        return redirect("empresa:inicio_sesion")

    try:
        perfil_empresa = PerfilEmpresa.objects.get(usuario=request.user)

        # Aquí iría la lógica para obtener las contraseñas guardadas
        # Por ahora, usamos una lista vacía
        contrasenas = []

        if request.method == "POST":
            # Procesar el formulario para agregar una nueva contraseña
            if "agregar_contrasena" in request.POST:
                # Aquí iría la lógica para guardar una nueva contraseña
                messages.success(request, "Contraseña guardada correctamente")
                return redirect("empresa:contrasenas")

            # Procesar la eliminación de una contraseña
            if "eliminar_contrasena" in request.POST:
                contrasena_id = request.POST.get("contrasena_id")
                # Aquí iría la lógica para eliminar la contraseña
                messages.success(request, "Contraseña eliminada correctamente")
                return redirect("empresa:contrasenas")

        context = {
            "perfil": perfil_empresa,
            "contrasenas": contrasenas,
        }
        return render(request, "empresa/contrasenas.html", context)

    except PerfilEmpresa.DoesNotExist:
        messages.error(request, "No se encontró el perfil de la empresa")
        return redirect("empresa:perfil")

@login_required
def dashboard_empresa(request):
    """Dashboard específico para empresas"""
    try:
        perfil_empresa = PerfilEmpresa.objects.get(usuario=request.user)
        return render(request, "empresa/dashboard.html", {"perfil": perfil_empresa})
    except PerfilEmpresa.DoesNotExist:
        messages.error(request, "No tienes un perfil de empresa asociado.")
        return redirect("Aplicacion:home")

@login_required
def cerrar_sesion(request):
    """Cierra la sesión del usuario y redirige a la página de inicio"""
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("empresa:home")

@login_required
def subir_documento(request):
    """Vista para subir documentos a la caja fuerte"""
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        messages.error(request, "Acceso restringido a empresas")
        return redirect("empresa:inicio_sesion")

    if request.method == "POST" and request.FILES.get("documento"):
        documento = request.FILES["documento"]
        descripcion = request.POST.get("descripcion", "")

        # Validar el tipo de archivo (opcional)
        extensiones_permitidas = [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".jpg", ".jpeg", ".png"]
        nombre_archivo = documento.name.lower()
        if not any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas):
            messages.error(request, "Tipo de archivo no permitido. Formatos aceptados: " +
                         ", ".join(ext[1:] for ext in extensiones_permitidas))
            return redirect("empresa:caja_fuerte")

        try:
            # Crear directorio si no existe
            upload_dir = os.path.join(settings.MEDIA_ROOT, "documentos", str(request.user.id))
            os.makedirs(upload_dir, exist_ok=True)

            # Generar nombre único para el archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{timestamp}_{documento.name}"
            ruta_archivo = os.path.join(upload_dir, nombre_archivo)

            # Guardar el archivo
            with open(ruta_archivo, "wb+") as destino:
                destino.writelines(documento.chunks())

            # Aquí podrías guardar la información del documento en tu modelo
            # Por ejemplo: Documento.objects.create(usuario=request.user, ruta=ruta_archivo, descripcion=descripcion)

            messages.success(request, "Documento subido correctamente")
            return redirect("empresa:caja_fuerte")

        except Exception as e:
            messages.error(request, f"Error al subir el documento: {e!s}")
            return redirect("empresa:caja_fuerte")

    return redirect("empresa:caja_fuerte")

@login_required
def ver_documento(request, documento_id):
    """Vista para ver un documento específico"""
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        messages.error(request, "Acceso restringido a empresas")
        return redirect("empresa:inicio_sesion")

    try:
        # Aquí deberías obtener el documento de tu modelo
        # Por ejemplo: documento = Documento.objects.get(id=documento_id, usuario=request.user)
        # Por ahora, asumiremos que el documento_id es el nombre del archivo

        # Construir la ruta al archivo
        file_path = os.path.join(settings.MEDIA_ROOT, "documentos", str(request.user.id), str(documento_id))

        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            raise Http404("El documento no existe o no tienes permiso para verlo")

        # Obtener la extensión del archivo
        _, file_extension = os.path.splitext(file_path)

        # Mapear extensiones a tipos MIME
        mime_types = {
            ".pdf": "application/pdf",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls": "application/vnd.ms-excel",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

        # Obtener el tipo MIME o usar 'application/octet-stream' como valor por defecto
        content_type = mime_types.get(file_extension.lower(), "application/octet-stream")

        # Devolver el archivo como respuesta
        response = FileResponse(open(file_path, "rb"), content_type=content_type)
        response["Content-Disposition"] = f'inline; filename="{os.path.basename(file_path)}"'
        return response

    except Exception as e:
        messages.error(request, f"Error al abrir el documento: {e!s}")
        return redirect("empresa:caja_fuerte")

@login_required
@require_POST
def eliminar_documento(request, documento_id):
    """Vista para eliminar un documento"""
    if not hasattr(request.user, "is_company") or not request.user.is_company:
        return JsonResponse({"success": False, "message": "Acceso no autorizado"}, status=403)

    try:
        # Construir la ruta al archivo
        file_path = os.path.join(settings.MEDIA_ROOT, "documentos", str(request.user.id), str(documento_id))

        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            return JsonResponse({"success": False, "message": "El documento no existe"}, status=404)

        # Aquí deberías verificar los permisos adicionales si es necesario
        # Por ejemplo, verificar que el documento pertenece al usuario

        # Eliminar el archivo
        os.remove(file_path)

        # Aquí podrías eliminar el registro de la base de datos si tienes un modelo
        # Por ejemplo: Documento.objects.filter(id=documento_id, usuario=request.user).delete()

        return JsonResponse({"success": True, "message": "Documento eliminado correctamente"})

    except Exception as e:
        return JsonResponse(
            {"success": False, "message": f"Error al eliminar el documento: {e!s}"},
            status=500,
        )

@require_http_methods(["GET"])
def obtener_ciudades(request):
    """Vista para obtener la lista de ciudades según el país seleccionado"""
    pais = request.GET.get("pais", "").lower()

    # Diccionario de países y sus ciudades
    ciudades_por_pais = {
        "colombia": [
            "Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena",
            "Cúcuta", "Bucaramanga", "Pereira", "Santa Marta", "Ibagué",
        ],
        "mexico": [
            "Ciudad de México", "Guadalajara", "Monterrey", "Puebla", "Tijuana",
            "León", "Zapopan", "Juárez", "Mérida", "Querétaro",
        ],
        "españa": [
            "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza",
            "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao",
        ],
        "argentina": [
            "Buenos Aires", "Córdoba", "Rosario", "Mendoza", "Tucumán",
            "La Plata", "Mar del Plata", "Salta", "Santa Fe", "San Juan",
        ],
    }

    # Obtener las ciudades para el país seleccionado o lista vacía si no existe
    ciudades = ciudades_por_pais.get(pais, [])

    return JsonResponse({"ciudades": ciudades})

@login_required
def perfil_empresa(request):
    """Vista del perfil de empresa"""
    try:
        perfil = PerfilEmpresa.objects.get(usuario=request.user)
        return render(request, "empresa/perfil.html", {"perfil": perfil})
    except PerfilEmpresa.DoesNotExist:
        messages.error(request, "No tienes un perfil de empresa asociado.")
        return redirect("Aplicacion:home")
