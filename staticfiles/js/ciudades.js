// Lista de ciudades por país
const ciudades = {
    'CO': [
        'Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena',
        'Cúcuta', 'Bucaramanga', 'Ibagué', 'Manizales', 'Pereira',
        'Neiva', 'Villavicencio', 'Sincelejo', 'Montería', 'Armenia',
        'Florencia', 'Popayán', 'Tunja', 'Valledupar', 'Ipiales'
    ],
    'US': [
        'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
        'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
        'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Indianapolis',
        'San Francisco', 'Seattle', 'Denver', 'Washington', 'Boston',
        'El Paso', 'Detroit', 'Nashville', 'Portland', 'Memphis'
    ],
    'MX': [
        'Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla', 'Toluca',
        'Tijuana', 'León', 'Juárez', 'Torreón', 'Mérida',
        'Querétaro', 'San Luis Potosí', 'Culiacán', 'Chihuahua', 'Saltillo',
        'Xalapa', 'Tampico', 'Aguascalientes', 'Córdoba', 'Oaxaca'
    ]
};

// Función para cargar ciudades según el país seleccionado
function cargarCiudades() {
    const pais = document.getElementById('empresa_pais').value;
    const selectCiudad = document.getElementById('empresa_ciudad');
    
    // Limpiar el select de ciudades
    selectCiudad.innerHTML = '<option value="">Seleccione...</option>';
    
    // Si hay un país seleccionado, cargar sus ciudades
    if (pais) {
        const ciudadesPais = ciudades[pais];
        if (ciudadesPais) {
            ciudadesPais.forEach(ciudad => {
                const option = document.createElement('option');
                option.value = ciudad;
                option.textContent = ciudad;
                selectCiudad.appendChild(option);
            });
        }
    }
}

// Agregar evento para cargar ciudades cuando cambie el país
document.addEventListener("DOMContentLoaded", function() {
    const selectPais = document.getElementById('empresa_pais');
    if (selectPais) {
        selectPais.addEventListener('change', cargarCiudades);
    }
});
