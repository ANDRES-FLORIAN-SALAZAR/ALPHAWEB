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
    const tipoRegistro = document.getElementById('tipo_registro');
    const camposNatural = document.getElementById('campos_natural');
    const camposEmpresa = document.getElementById('campos_empresa');

    if (tipoRegistro && camposNatural && camposEmpresa) {
        console.log('Elementos encontrados');
        
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
    } else {
        console.error('No se encontraron los elementos necesarios en mostrarCampos');
    }
}
