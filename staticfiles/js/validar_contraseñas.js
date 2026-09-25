// Validación de contraseñas
const password1 = document.querySelector('input[name="password1"]');
const password2 = document.querySelector('input[name="password2"]');
const botonEnviar = document.getElementById('btn-registro');

if (password1 && password2) {
    // Validar que las contraseñas coincidan
    function validarContraseñas() {
        if (password1.value !== password2.value) {
            password1.style.borderColor = 'red';
            password2.style.borderColor = 'red';
            botonEnviar.disabled = true;
        } else {
            password1.style.borderColor = '';
            password2.style.borderColor = '';
            botonEnviar.disabled = false;
            botonEnviar.disabled = false;
        }
    }

    // Agregar eventos de escucha
    password1.addEventListener('input', validarContraseñas);
    password2.addEventListener('input', validarContraseñas);

    // Validar inicialmente
    validarContraseñas();
}
