// static/js/registro.js

// Función para mostrar/ocultar campos según el tipo de registro
function mostrarCampos() {
    const tipoRegistro = document.getElementById('tipo_registro').value;
    const camposNatural = document.getElementById('campos_natural');
    const camposEmpresa = document.getElementById('campos_empresa');
    
    // Ocultar ambos grupos de campos
    camposNatural.style.display = 'none';
    camposEmpresa.style.display = 'none';
    
    // Mostrar el grupo correspondiente
    if (tipoRegistro === 'natural') {
        camposNatural.style.display = 'block';
    } else if (tipoRegistro === 'empresa') {
        camposEmpresa.style.display = 'block';
    }
}

// Función para alternar la visibilidad de la contraseña
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.password-toggle-btn');
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
}

// Validación de coincidencia de contraseñas
function validatePasswords() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const passwordMatch = document.getElementById('password-match');
    
    if (password1 && password2 && passwordMatch) {
        if (password1.value !== password2.value && password2.value !== '') {
            password2.classList.add('is-invalid');
            passwordMatch.classList.add('show');
            return false;
        } else {
            password2.classList.remove('is-invalid');
            passwordMatch.classList.remove('show');
            return true;
        }
    }
    return true;
}

function validateEmpresaPasswords() {
    const passwordEmpresa = document.getElementById('password_empresa');
    const confirmPasswordEmpresa = document.getElementById('confirmar_password_empresa');
    const passwordEmpresaMatch = document.getElementById('password-empresa-match');
    
    if (passwordEmpresa && confirmPasswordEmpresa && passwordEmpresaMatch) {
        if (passwordEmpresa.value !== confirmPasswordEmpresa.value && confirmPasswordEmpresa.value !== '') {
            confirmPasswordEmpresa.classList.add('is-invalid');
            passwordEmpresaMatch.classList.add('show');
            return false;
        } else {
            confirmPasswordEmpresa.classList.remove('is-invalid');
            passwordEmpresaMatch.classList.remove('show');
            return true;
        }
    }
    return true;
}

// Event listeners para validar las contraseñas mientras se escriben
function setupPasswordValidation() {
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    const passwordEmpresa = document.getElementById('password_empresa');
    const confirmPasswordEmpresa = document.getElementById('confirmar_password_empresa');
    
    if (password1 && password2) {
        password1.addEventListener('input', validatePasswords);
        password2.addEventListener('input', validatePasswords);
    }
    
    if (passwordEmpresa && confirmPasswordEmpresa) {
        passwordEmpresa.addEventListener('input', validateEmpresaPasswords);
        confirmPasswordEmpresa.addEventListener('input', validateEmpresaPasswords);
    }
}

// Función para validar campos requeridos
function validateRequiredField(fieldId, errorMessage) {
    const field = document.getElementById(fieldId);
    if (!field) return true;
    
    if (!field.value.trim()) {
        field.classList.add('is-invalid');
        console.log(errorMessage);
        return false;
    } else {
        field.classList.remove('is-invalid');
        return true;
    }
}

// Validación del formulario antes de enviar
function setupFormValidation() {
    const form = document.getElementById('form-registro');
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
        const tipoRegistro = document.getElementById('tipo_registro').value;
        let isValid = true;
        
        // Limpiar errores previos
        document.querySelectorAll('.is-invalid').forEach(el => {
            el.classList.remove('is-invalid');
        });
        
        // Validar según el tipo de registro
        if (tipoRegistro === 'natural') {
            isValid &= validateRequiredField('nombre_completo', 'Nombre completo es requerido');
            isValid &= validateRequiredField('email', 'Email es requerido');
            isValid &= validateRequiredField('telefono', 'Teléfono es requerido');
            isValid &= validateRequiredField('edad', 'Edad es requerida');
            isValid &= validateRequiredField('password1', 'Contraseña es requerida');
            
            // Validar coincidencia de contraseñas
            if (!validatePasswords()) {
                isValid = false;
            }
            
        } else if (tipoRegistro === 'empresa') {
            isValid &= validateRequiredField('razon_social', 'Razón social es requerida');
            isValid &= validateRequiredField('nit', 'NIT es requerido');
            isValid &= validateRequiredField('email_empresa', 'Email de empresa es requerido');
            isValid &= validateRequiredField('telefono_empresa', 'Teléfono de empresa es requerido');
            isValid &= validateRequiredField('direccion', 'Dirección es requerida');
            isValid &= validateRequiredField('representante_legal', 'Representante legal es requerido');
            isValid &= validateRequiredField('password_empresa', 'Contraseña es requerida');
            
            // Validar coincidencia de contraseñas
            if (!validateEmpresaPasswords()) {
                isValid = false;
            }
            
        } else {
            alert('Por favor seleccione un tipo de registro');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
            // Desplazarse al primer campo con error
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstInvalid.focus();
            }
        }
    });
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    mostrarCampos();
    setupPasswordValidation();
    setupFormValidation();
    
    // Setup del selector de tipo de registro
    const tipoSelect = document.getElementById('tipo_registro');
    if (tipoSelect) {
        tipoSelect.addEventListener('change', mostrarCampos);
    }
});