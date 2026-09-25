// Validación de contraseñas para personas naturales
const password1 = document.querySelector('input[name="password1"]');
const password2 = document.querySelector('input[name="password2"]');
const passwordMatchMessage = document.getElementById('password-match');

if (password1 && password2) {
    // Validar que las contraseñas coincidan
    function validarContraseñas() {
        // Solo mostrar el mensaje si ambos campos tienen contenido
        if (password1.value && password2.value) {
            if (password1.value !== password2.value) {
                password1.style.borderColor = 'red';
                password2.style.borderColor = 'red';
                if (passwordMatchMessage) {
                    passwordMatchMessage.style.display = 'block';
                    passwordMatchMessage.textContent = 'Las contraseñas no coinciden';
                }
            } else {
                password1.style.borderColor = 'green';
                password2.style.borderColor = 'green';
                if (passwordMatchMessage) {
                    passwordMatchMessage.style.display = 'none';
                }
            }
        } else {
            // Si uno de los campos está vacío, limpiar estilos y ocultar mensaje
            password1.style.borderColor = '';
            password2.style.borderColor = '';
            if (passwordMatchMessage) {
                passwordMatchMessage.style.display = 'none';
            }
        }
    }

    // Agregar eventos de escucha
    password1.addEventListener('input', validarContraseñas);
    password2.addEventListener('input', validarContraseñas);
}

// Validación de contraseñas para empresas
const passwordEmpresa = document.querySelector('input[name="password_empresa"]');
const confirmarPasswordEmpresa = document.querySelector('input[name="confirmar_password_empresa"]');
const passwordEmpresaMatchMessage = document.getElementById('password-empresa-match');

if (passwordEmpresa && confirmarPasswordEmpresa) {
    function validarContraseñasEmpresa() {
        // Solo mostrar el mensaje si ambos campos tienen contenido
        if (passwordEmpresa.value && confirmarPasswordEmpresa.value) {
            if (passwordEmpresa.value !== confirmarPasswordEmpresa.value) {
                passwordEmpresa.style.borderColor = 'red';
                confirmarPasswordEmpresa.style.borderColor = 'red';
                if (passwordEmpresaMatchMessage) {
                    passwordEmpresaMatchMessage.style.display = 'block';
                    passwordEmpresaMatchMessage.textContent = 'Las contraseñas no coinciden';
                }
            } else {
                passwordEmpresa.style.borderColor = 'green';
                confirmarPasswordEmpresa.style.borderColor = 'green';
                if (passwordEmpresaMatchMessage) {
                    passwordEmpresaMatchMessage.style.display = 'none';
                }
            }
        } else {
            // Si uno de los campos está vacío, limpiar estilos y ocultar mensaje
            passwordEmpresa.style.borderColor = '';
            confirmarPasswordEmpresa.style.borderColor = '';
            if (passwordEmpresaMatchMessage) {
                passwordEmpresaMatchMessage.style.display = 'none';
            }
        }
    }

    // Agregar eventos de escucha
    passwordEmpresa.addEventListener('input', validarContraseñasEmpresa);
    confirmarPasswordEmpresa.addEventListener('input', validarContraseñasEmpresa);
}
