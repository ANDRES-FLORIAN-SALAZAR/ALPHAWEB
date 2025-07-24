// Añadir depuración para el envío del formulario
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-registro');
    const btnRegistro = document.getElementById('btn-registro');

    if (form && btnRegistro) {
        console.log('Formulario y botón encontrados');
        
        // Mostrar campos iniciales
        mostrarCampos();

        // Agregar evento al botón
        btnRegistro.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Botón de registro clickeado');
            
            // Verificar si el formulario es válido
            if (form.checkValidity()) {
                console.log('Formulario válido');
                form.submit();
            } else {
                console.log('Formulario inválido');
                form.reportValidity();
            }
        });
    } else {
        console.log('No se encontró el formulario o el botón');
    }
});

// Función para mostrar/ocultar campos según el tipo de registro
function mostrarCampos() {
    const tipoUsuario = document.getElementById('tipo_registro').value;
    const camposNatural = document.getElementById('campos_natural');
    const camposEmpresa = document.getElementById('campos_empresa');
    const btnRegistro = document.getElementById('btn-registro');
    const form = document.getElementById('form-registro');

    console.log('Mostrar campos para:', tipoUsuario);

    // Mostrar/ocultar secciones según el tipo de usuario
    if (tipoUsuario === 'natural') {
        camposNatural.style.display = 'block';
        camposEmpresa.style.display = 'none';
        if (btnRegistro) btnRegistro.textContent = 'Registrarse como Persona Natural';
    } else if (tipoUsuario === 'empresa') {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'block';
        if (btnRegistro) btnRegistro.textContent = 'Registrar Empresa';
        
        // Inicializar la validación de empleados cuando se muestran los campos de empresa
        if (window.inicializarValidacionEmpleados) {
            setTimeout(function() {
                inicializarValidacionEmpleados();
                // Forzar la validación del formulario
                if (form) form.classList.add('was-validated');
            }, 100);
        }
    } else {
        camposNatural.style.display = 'none';
        camposEmpresa.style.display = 'none';
        if (btnRegistro) btnRegistro.textContent = 'Seleccione un tipo de registro';
    }
    
    // Restablecer la validación del formulario
    if (form) {
        form.classList.remove('was-validated');
    }
}
