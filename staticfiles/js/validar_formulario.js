// Validación del formulario de registro
function validarFormulario() {
    limpiarMensajesError(); // Limpia errores anteriores antes de validar

    const tipoRegistro = document.getElementById("tipo_registro");
    if (!tipoRegistro || !tipoRegistro.value) {
        mostrarMensajeError("Por favor, seleccione el tipo de registro");
        return false;
    }

    let camposValidos = true;

    // Validar campos comunes
    const camposComunes = [
        { 
            selector: "input[name='nombre_completo']", 
            mensaje: "Por favor, ingrese su nombre completo",
            required: true
        },
        { 
            selector: "input[name='email']", 
            mensaje: "Por favor, ingrese un correo electrónico válido",
            pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            required: true
        },
        { 
            selector: "input[name='password1']", 
            mensaje: "Por favor, ingrese una contraseña",
            min: 8,
            required: true
        },
        { 
            selector: "input[name='password2']", 
            mensaje: "Por favor, confirme su contraseña",
            required: true
        }
    ];

    camposValidos = validarCampos(camposComunes) && camposValidos;

    // Validar que las contraseñas coincidan
    const password1 = document.querySelector("input[name='password1']");
    const password2 = document.querySelector("input[name='password2']");
    if (password1 && password2 && password1.value !== password2.value) {
        mostrarMensajeError("Las contraseñas no coinciden");
        camposValidos = false;
    }

    // Validar campos específicos según el tipo de registro
    if (tipoRegistro.value === "natural") {
        const genero = document.querySelector("select[name='genero']");
        if (genero && !genero.value) {
            mostrarMensajeError("Por favor, seleccione su género");
            camposValidos = false;
        }
    } else if (tipoRegistro.value === "empresa") {
        const camposEmpresa = [
            { 
                selector: "input[name='empresa_nombre']", 
                mensaje: "Por favor, ingrese el nombre de la empresa",
                required: true
            },
            { 
                selector: "input[name='empresa_nit']", 
                mensaje: "Por favor, ingrese el NIT de la empresa",
                required: true
            },
            { 
                selector: "input[name='empresa_razon_social']", 
                mensaje: "Por favor, ingrese la razón social de la empresa",
                required: true
            },
            { 
                selector: "select[name='empresa_tipo']", 
                mensaje: "Por favor, seleccione el tipo de empresa",
                required: true
            },
            { 
                selector: "select[name='empresa_segmento']", 
                mensaje: "Por favor, seleccione el segmento de la empresa",
                required: true
            },
            { 
                selector: "select[name='empresa_tamaño']", 
                mensaje: "Por favor, seleccione el tamaño de la empresa",
                required: true
            },
            { 
                selector: "select[name='empresa_pais']", 
                mensaje: "Por favor, seleccione el país",
                required: true
            },
            { 
                selector: "select[name='empresa_ciudad']", 
                mensaje: "Por favor, seleccione la ciudad",
                required: true
            },
            { 
                selector: "input[name='empresa_direccion']", 
                mensaje: "Por favor, ingrese la dirección de la empresa",
                required: true
            }
        ];

        camposValidos = validarCampos(camposEmpresa) && camposValidos;
    }

    return camposValidos;
}

// Evento para validar el formulario antes de enviar
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('form-registro');
    const botonEnviar = document.getElementById('btn-registro');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // Evita el envío por defecto
            
            if (validarFormulario()) {
                // Si la validación es exitosa, permite el envío
                form.submit();
            }
        });
    }
});

// Función para mostrar/ocultar campos según el tipo de registro
function mostrarCampos() {
    const tipoRegistro = document.getElementById('tipo_registro');
    const camposNatural = document.getElementById('campos_natural');
    const camposEmpresa = document.getElementById('campos_empresa');
    
    if (tipoRegistro.value === 'natural') {
        camposNatural.style.display = 'block';
        camposEmpresa.style.display = 'none';
    } else if (tipoRegistro.value === 'empresa') {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'block';
    } else {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'none';
    }
}

// Función para mostrar mensajes de error en el formulario
function mostrarMensajeError(mensaje) {
    const mensajeError = document.createElement('div');
    mensajeError.className = 'alert alert-danger';
    mensajeError.textContent = mensaje;
    
    const form = document.getElementById('form-registro');
    if (form) {
        form.insertBefore(mensajeError, form.firstChild);
    }
    
    // Remover el mensaje después de 5 segundos
    setTimeout(() => {
        mensajeError.remove();
    }, 5000);
}

// ✅ NUEVA: Limpiar todos los mensajes de error antes de validar
function limpiarMensajesError() {
    const mensajes = document.querySelectorAll('.alert.alert-danger');
    mensajes.forEach(el => el.remove());
}

// ✅ NUEVA: Función modular para validar múltiples campos
function validarCampos(listaCampos) {
    let validos = true;
    listaCampos.forEach(campo => {
        const el = document.querySelector(campo.selector);
        if (el) {
            if (campo.required && !el.value.trim()) {
                mostrarMensajeError(campo.mensaje);
                validos = false;
            }
            if (campo.pattern && !el.value.match(campo.pattern)) {
                mostrarMensajeError(campo.mensaje);
                validos = false;
            }
            if (campo.min && el.value.length < campo.min) {
                mostrarMensajeError("La contraseña debe tener al menos 8 caracteres");
                validos = false;
            }
        }
    });
    return validos;
}
