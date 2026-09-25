// Añadir depuración para el envío del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-registro');

    if (form) {
        console.log('Formulario encontrado');

        // Mostrar campos iniciales
        mostrarCampos();
    } else {
        console.log('No se encontró el formulario');
    }
});

// Función para mostrar/ocultar campos según el tipo de registro
function mostrarCampos() {
    const tipoUsuario = document.getElementById('tipo_registro').value;
    const camposNatural = document.getElementById('campos_natural');
    const camposEmpresa = document.getElementById('campos_empresa');
    const form = document.getElementById('form-registro');

    console.log('Mostrar campos para:', tipoUsuario);

    // Remover atributo required de todos los campos primero
    const allInputs = form.querySelectorAll('input, select, textarea');
    allInputs.forEach(input => {
        input.removeAttribute('required');
    });

    // Mostrar/ocultar secciones según el tipo de usuario
    if (tipoUsuario === 'natural') {
        camposNatural.style.display = 'block';
        camposEmpresa.style.display = 'none';

        // Agregar required solo a campos de persona natural
        const naturalInputs = camposNatural.querySelectorAll('input, select, textarea');
        naturalInputs.forEach(input => {
            if (input.hasAttribute('data-required')) {
                input.setAttribute('required', 'required');
            }
        });

    } else if (tipoUsuario === 'empresa') {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'block';

        // Agregar required solo a campos de empresa
        const empresaInputs = camposEmpresa.querySelectorAll('input, select, textarea');
        empresaInputs.forEach(input => {
            if (input.hasAttribute('data-required')) {
                input.setAttribute('required', 'required');
            }
        });

        // Inicializar la validación de empleados cuando se muestran los campos de empresa
        if (window.inicializarValidacionEmpleados) {
            setTimeout(function() {
                inicializarValidacionEmpleados();
            }, 100);
        }
    } else {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'none';
    }

    // Restablecer la validación del formulario
    if (form) {
        form.classList.remove('was-validated');
    }
}
