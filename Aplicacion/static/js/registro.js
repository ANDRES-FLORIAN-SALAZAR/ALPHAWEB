// static/js/registro.js

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

    // NO prevenir el envío del formulario, dejar que Django maneje la validación
    // Solo agregar validación visual de contraseñas
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    setupPasswordValidation();
    setupFormValidation();
});