// Lista de países con sus códigos y nombres
const paises = {
    'AF': 'Afganistán',
    'AX': 'Islas de Åland',
    'AL': 'Albania',
    'DZ': 'Argelia',
    'AS': 'Samoa Americana',
    'AD': 'Andorra',
    'AO': 'Angola',
    'AI': 'Anguila',
    'AQ': 'Antártida',
    'AG': 'Antigua y Barbuda',
    'AR': 'Argentina',
    'AM': 'Armenia',
    'AW': 'Aruba',
    'AU': 'Australia',
    'AT': 'Austria',
    'AZ': 'Azerbaiyán',
    'BS': 'Bahamas',
    'BH': 'Baréin',
    'BD': 'Bangladesh',
    'BB': 'Barbados',
    'BY': 'Bielorrusia',
    'BE': 'Bélgica',
    'BZ': 'Belice',
    'BJ': 'Benín',
    'BM': 'Bermudas',
    'BT': 'Bután',
    'BO': 'Bolivia',
    'BA': 'Bosnia y Herzegovina',
    'BW': 'Botsuana',
    'BV': 'Isla Bouvet',
    'BR': 'Brasil',
    'IO': 'Territorio Británico del Océano Índico',
    'BN': 'Brunei',
    'BG': 'Bulgaria',
    'BF': 'Burkina Faso',
    'BI': 'Burundi',
    'CV': 'Cabo Verde',
    'KH': 'Camboya',
    'CM': 'Camerún',
    'CA': 'Canadá',
    'KY': 'Islas Caimán',
    'CF': 'República Centroafricana',
    'TD': 'Chad',
    'CL': 'Chile',
    'CN': 'China',
    'CX': 'Isla de Navidad',
    'CC': 'Islas Cocos',
    'CO': 'Colombia',
    'KM': 'Comoras',
    'CG': 'Congo',
    'CD': 'República Democrática del Congo',
    'CK': 'Islas Cook',
    'CR': 'Costa Rica',
    'CI': 'Costa de Marfil',
    'HR': 'Croacia',
    'CU': 'Cuba',
    'CW': 'Curazao',
    'CY': 'Chipre',
    'CZ': 'República Checa',
    'DK': 'Dinamarca',
    'DJ': 'Yibuti',
    'DM': 'Dominica',
    'DO': 'República Dominicana',
    'EC': 'Ecuador',
    'EG': 'Egipto',
    'SV': 'El Salvador',
    'GQ': 'Guinea Ecuatorial',
    'ER': 'Eritrea',
    'EE': 'Estonia',
    'ET': 'Etiopía',
    'FK': 'Islas Malvinas',
    'FO': 'Islas Feroe',
    'FJ': 'Fiyi',
    'FI': 'Finlandia',
    'FR': 'Francia',
    'GF': 'Guayana Francesa',
    'PF': 'Polinesia Francesa',
    'TF': 'Territorios Franceses del Sur',
    'GA': 'Gabón',
    'GM': 'Gambia',
    'GE': 'Georgia',
    'DE': 'Alemania',
    'GH': 'Ghana',
    'GI': 'Gibraltar',
    'GR': 'Grecia',
    'GL': 'Groenlandia',
    'GD': 'Granada',
    'GP': 'Guadalupe',
    'GU': 'Guam',
    'GT': 'Guatemala',
    'GG': 'Guernsey',
    'GN': 'Guinea',
    'GW': 'Guinea-Bissau',
    'GY': 'Guyana',
    'HT': 'Haití',
    'HM': 'Islas Heard y McDonald',
    'VA': 'Ciudad del Vaticano',
    'HN': 'Honduras',
    'HK': 'Hong Kong',
    'HU': 'Hungría',
    'IS': 'Islandia',
    'IN': 'India',
    'ID': 'Indonesia',
    'IR': 'Irán',
    'IQ': 'Iraq',
    'IE': 'Irlanda',
    'IM': 'Isla de Man',
    'IL': 'Israel',
    'IT': 'Italia',
    'JM': 'Jamaica',
    'JP': 'Japón',
    'JE': 'Jersey',
    'JO': 'Jordania',
    'KZ': 'Kazajistán',
    'KE': 'Kenia',
    'KI': 'Kiribati',
    'KP': 'Corea del Norte',
    'KR': 'Corea del Sur',
    'KW': 'Kuwait',
    'KG': 'Kirguistán',
    'LA': 'Laos',
    'LV': 'Letonia',
    'LB': 'Líbano',
    'LS': 'Lesoto',
    'LR': 'Liberia',
    'LY': 'Libia',
    'LI': 'Liechtenstein',
    'LT': 'Lituania',
    'LU': 'Luxemburgo',
    'MO': 'Macao',
    'MK': 'Macedonia del Norte',
    'MG': 'Madagascar',
    'MW': 'Malawi',
    'MY': 'Malasia',
    'MV': 'Maldivas',
    'ML': 'Malí',
    'MT': 'Malta',
    'MH': 'Islas Marshall',
    'MQ': 'Martinica',
    'MR': 'Mauritania',
    'MU': 'Mauricio',
    'YT': 'Mayotte',
    'MX': 'México',
    'FM': 'Micronesia',
    'MD': 'Moldavia',
    'MC': 'Mónaco',
    'MN': 'Mongolia',
    'ME': 'Montenegro',
    'MS': 'Montserrat',
    'MA': 'Marruecos',
    'MZ': 'Mozambique',
    'MM': 'Myanmar',
    'NA': 'Namibia',
    'NR': 'Nauru',
    'NP': 'Nepal',
    'NL': 'Países Bajos',
    'NC': 'Nueva Caledonia',
    'NZ': 'Nueva Zelanda',
    'NI': 'Nicaragua',
    'NE': 'Níger',
    'NG': 'Nigeria',
    'NU': 'Niue',
    'NF': 'Isla Norfolk',
    'MP': 'Islas Marianas del Norte',
    'NO': 'Noruega',
    'OM': 'Omán',
    'PK': 'Pakistán',
    'PW': 'Palau',
    'PS': 'Territorios Palestinos',
    'PA': 'Panamá',
    'PG': 'Papúa Nueva Guinea',
    'PY': 'Paraguay',
    'PE': 'Perú',
    'PH': 'Filipinas',
    'PN': 'Islas Pitcairn',
    'PL': 'Polonia',
    'PT': 'Portugal',
    'PR': 'Puerto Rico',
    'QA': 'Catar',
    'RE': 'Reunión',
    'RO': 'Rumania',
    'RU': 'Rusia',
    'RW': 'Ruanda',
    'BL': 'San Bartolomé',
    'SH': 'Santa Helena',
    'KN': 'San Cristóbal y Nieves',
    'LC': 'Santa Lucía',
    'MF': 'San Martín',
    'PM': 'San Pedro y Miquelón',
    'VC': 'San Vicente y las Granadinas',
    'WS': 'Samoa',
    'SM': 'San Marino',
    'ST': 'Santo Tomé y Príncipe',
    'SA': 'Arabia Saudita',
    'SN': 'Senegal',
    'RS': 'Serbia',
    'SC': 'Seychelles',
    'SL': 'Sierra Leona',
    'SG': 'Singapur',
    'SX': 'Sint Maarten',
    'SK': 'Eslovaquia',
    'SI': 'Eslovenia',
    'SB': 'Islas Salomón',
    'SO': 'Somalia',
    'ZA': 'Sudáfrica',
    'GS': 'Georgia del Sur y las Islas Sandwich del Sur',
    'SS': 'Sudán del Sur',
    'ES': 'España',
    'LK': 'Sri Lanka',
    'SD': 'Sudán',
    'SR': 'Surinam',
    'SJ': 'Svalbard y Jan Mayen',
    'SZ': 'Suazilandia',
    'SE': 'Suecia',
    'CH': 'Suiza',
    'SY': 'Siria',
    'TW': 'Taiwán',
    'TJ': 'Tayikistán',
    'TZ': 'Tanzania',
    'TH': 'Tailandia',
    'TL': 'Timor Oriental',
    'TG': 'Togo',
    'TK': 'Tokelau',
    'TO': 'Tonga',
    'TT': 'Trinidad y Tobago',
    'TN': 'Túnez',
    'TR': 'Turquía',
    'TM': 'Turkmenistán',
    'TC': 'Islas Turcas y Caicos',
    'TV': 'Tuvalu',
    'UG': 'Uganda',
    'UA': 'Ucrania',
    'AE': 'Emiratos Árabes Unidos',
    'GB': 'Reino Unido',
    'US': 'Estados Unidos',
    'UM': 'Islas Ultramarinas Menores de Estados Unidos',
    'UY': 'Uruguay',
    'UZ': 'Uzbekistán',
    'VU': 'Vanuatu',
    'VE': 'Venezuela',
    'VN': 'Vietnam',
    'VG': 'Islas Vírgenes Británicas',
    'VI': 'Islas Vírgenes de los Estados Unidos',
    'WF': 'Wallis y Futuna',
    'EH': 'Sahara Occidental',
    'YE': 'Yemen',
    'ZM': 'Zambia',
    'ZW': 'Zimbabue'
};

// Lista de ciudades por país (ciudades principales)
const ciudades = {
    // América
    'AR': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata', 'Mar del Plata', 'Salta', 'Tucumán', 'Santa Fe', 'Resistencia'],
    'BO': ['La Paz', 'Santa Cruz', 'Cochabamba', 'El Alto', 'Oruro', 'Potosí', 'Tarija', 'Sucre', 'Trinidad', 'Yacuiba'],
    'BR': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza', 'Belo Horizonte', 'Manaus', 'Curitiba', 'Recife', 'Porto Alegre'],
    'CA': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Québec', 'Hamilton', 'Kitchener'],
    'CL': ['Santiago', 'Concepción', 'Valparaíso', 'La Serena', 'Antofagasta', 'Talca', 'Temuco', 'Valdivia', 'Puerto Montt', 'Iquique'],
    'CO': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Cúcuta', 'Bucaramanga', 'Ibagué', 'Manizales', 'Pereira'],
    'MX': ['Ciudad de México', 'Guadalajara', 'Monterrey', 'Puebla', 'Toluca', 'Tijuana', 'León', 'Juárez', 'Torreón', 'Mérida'],
    'US': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'],
    
    // Europa
    'ES': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Zaragoza', 'Málaga', 'Murcia', 'Palma de Mallorca', 'Las Palmas de Gran Canaria', 'Bilbao'],
    'FR': ['París', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille'],
    'GB': ['Londres', 'Birmingham', 'Manchester', 'Leeds', 'Glasgow', 'Sheffield', 'Bradford', 'Liverpool', 'Edinburgh', 'Bristol'],
    'DE': ['Berlín', 'Hamburgo', 'Múnich', 'Cologne', 'Frankfurt', 'Stuttgart', 'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig'],
    
    // Asia
    'CN': ['Pekín', 'Shanghái', 'Guangzhou', 'Shenzhen', 'Tianjin', 'Chongqing', 'Chengdu', 'Wuhan', 'Hangzhou', 'Nanjing'],
    'JP': ['Tokio', 'Yokohama', 'Osaka', 'Nagoya', 'Sapporo', 'Kobe', 'Kawasaki', 'Kyoto', 'Fukuoka', 'Hiroshima'],
    'IN': ['Nueva Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Surat', 'Pune', 'Jaipur'],
    
    // Oceanía
    'AU': ['Sídney', 'Melbourne', 'Brisbane', 'Adelaide', 'Perth', 'Gold Coast', 'Canberra', 'Newcastle', 'Wollongong', 'Sunshine Coast'],
    
    // África
    'EG': ['El Cairo', 'Alejandría', 'Port Said', 'Suez', 'Luxor', 'Aswan', 'Giza', 'Damanhur', 'Zagazig', 'Beni Suef'],
    'ZA': ['Ciudad del Cabo', 'Johannesburgo', 'Durban', 'Pretoria', 'Pietermaritzburg', 'Port Elizabeth', 'East London', 'Bloemfontein', 'Kimberley', 'Mafikeng']
};

// Función para cargar ciudades según el país seleccionado
function cargarCiudades() {
    const pais = document.getElementById('empresa_pais').value;
    const selectCiudad = document.getElementById('empresa_ciudad');
    
    // Limpiar el select de ciudades
    selectCiudad.innerHTML = '<option value="">Seleccione...</option>';
    
    // Si hay un país seleccionado, cargar sus ciudades
    if (pais && ciudades[pais]) {
        ciudades[pais].forEach(ciudad => {
            const option = document.createElement('option');
            option.value = ciudad;
            option.textContent = ciudad;
            selectCiudad.appendChild(option);
        });
    }
}

// Agregar evento para cargar ciudades cuando cambie el país
document.addEventListener("DOMContentLoaded", function() {
    const selectPais = document.getElementById('empresa_pais');
    const selectCiudad = document.getElementById('empresa_ciudad');
    
    if (selectPais && selectCiudad) {
        selectPais.addEventListener('change', cargarCiudades);
        // Cargar las ciudades si ya hay un país seleccionado
        if (selectPais.value) {
            cargarCiudades();
        }
    }
});

// Función para actualizar el select de países con la lista completa
function actualizarSelectPaises() {
    const selectPais = document.getElementById('empresa_pais');
    if (selectPais) {
        // Limpiar el select
        selectPais.innerHTML = '<option value="">Seleccione...</option>';
        
        // Agregar los países en orden alfabético
        Object.entries(paises).sort(([code1, name1], [code2, name2]) => name1.localeCompare(name2)).forEach(([code, name]) => {
            const option = document.createElement('option');
            option.value = code;
            option.textContent = name;
            selectPais.appendChild(option);
        });
    }
}

// Actualizar el select de países cuando se cargue la página
document.addEventListener("DOMContentLoaded", actualizarSelectPaises);
