// Función para inicializar la validación de empleados
function inicializarValidacionEmpleados() {
    const tamañoSelect = document.getElementById("empresa_tamaño");
    const empleadosInput = document.getElementById("empresa_numero_empleados");

    if (!tamañoSelect || !empleadosInput) {
        console.error('No se encontraron los elementos necesarios para la validación de empleados');
        return;
    }

    function actualizarLimites() {
        const valor = tamañoSelect.value;
        console.log('Tamaño de empresa seleccionado:', valor);

        if (valor === "micro") {
            empleadosInput.min = 1;
            empleadosInput.max = 10;
            empleadosInput.placeholder = "1-10 empleados";
            console.log('Límites actualizados: 1-10 empleados');
        } else if (valor === "pequena") {
            empleadosInput.min = 11;
            empleadosInput.max = 50;
            empleadosInput.placeholder = "11-50 empleados";
            console.log('Límites actualizados: 11-50 empleados');
        } else if (valor === "mediana") {
            empleadosInput.min = 51;
            empleadosInput.max = 250;
            empleadosInput.placeholder = "51-250 empleados";
            console.log('Límites actualizados: 51-250 empleados');
        } else if (valor === "grande") {
            empleadosInput.min = 251;
            empleadosInput.removeAttribute("max");
            empleadosInput.placeholder = "251+ empleados";
            console.log('Límites actualizados: 251+ empleados');
        }

        // Forzar la validación del valor actual
        empleadosInput.reportValidity();
    }

    // Agregar validación personalizada
    empleadosInput.addEventListener('input', function() {
        const valor = parseInt(this.value);
        const min = parseInt(this.min) || 1;
        const max = parseInt(this.max) || Infinity;
        
        if (valor < min) {
            this.setCustomValidity(`El número mínimo de empleados es ${min}`);
        } else if (valor > max && !isNaN(max)) {
            this.setCustomValidity(`El número máximo de empleados es ${max}`);
        } else {
            this.setCustomValidity('');
        }
    });

    // Configurar el evento de cambio
    tamañoSelect.addEventListener("change", actualizarLimites);
    
    // Ejecutar al cargar la página
    document.addEventListener('DOMContentLoaded', actualizarLimites);
    
    // También ejecutar después de que se muestren los campos de empresa
    window.mostrarCampos = function() {
        // Esperar un momento para que se actualice el DOM
        setTimeout(actualizarLimites, 100);
    };

    // Inicializar ahora mismo si es posible
    actualizarLimites();
}

// Función para validar el número de empleados en tiempo real
function validarNumeroEmpleados(input) {
    const valor = parseInt(input.value);
    const min = parseInt(input.min) || 1;
    const max = parseInt(input.max) || Infinity;
    
    if (isNaN(valor) || valor < min) {
        input.setCustomValidity(`El número mínimo de empleados es ${min}`);
    } else if (valor > max && !isNaN(max)) {
        input.setCustomValidity(`El número máximo de empleados es ${max}`);
    } else {
        input.setCustomValidity('');
    }
    
    input.reportValidity();
}

// Hacer la función accesible globalmente
window.validarNumeroEmpleados = validarNumeroEmpleados;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', inicializarValidacionEmpleados);
