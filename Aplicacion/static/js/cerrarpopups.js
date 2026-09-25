// Función para cerrar popup cuando se hace clic fuera del contenido
function closePopup(event) {
    // Si el clic fue en el overlay (fondo oscuro), cerrar el popup
    if (event.target.classList.contains('overlay')) {
        // Remover el hash de la URL para cerrar el popup
        window.location.hash = '';
        // Alternativa: usar history.back() si prefieres
        // history.back();
    }
}

// Función para cerrar popup cuando se hace clic en la X
function closePopupX(popupId) {
    window.location.hash = '';
}

// Event listener para cerrar popup con la tecla Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        // Si hay un popup abierto (hash en la URL), cerrarlo
        if (window.location.hash.includes('popup')) {
            window.location.hash = '';
        }
    }
});

// Event listeners para todos los botones de cerrar (X)
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todos los botones de cerrar
    const closeButtons = document.querySelectorAll('.popup-card .close');
    
    closeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            window.location.hash = '';
        });
    });
    
    // Event listeners para los overlays
    const overlays = document.querySelectorAll('.overlay');
    
    overlays.forEach(function(overlay) {
        overlay.addEventListener('click', function(event) {
            // Solo cerrar si se hizo clic en el overlay, no en el contenido
            if (event.target === overlay) {
                window.location.hash = '';
            }
        });
    });
    
    // Event listeners para los botones de cookies
    const acceptButton = document.querySelector('.btn-accept');
    const customButton = document.querySelector('.btn-custom');
    const rejectButton = document.querySelector('.btn-reject');
    
    if (acceptButton) {
        acceptButton.addEventListener('click', function() {
            // Lógica para aceptar todas las cookies
            console.log('Cookies aceptadas');
            window.location.hash = '';
        });
    }
    
    if (customButton) {
        customButton.addEventListener('click', function() {
            // Lógica para personalizar cookies
            console.log('Personalizar cookies');
            // Aquí podrías abrir otro popup o formulario
        });
    }
    
    if (rejectButton) {
        rejectButton.addEventListener('click', function() {
            // Lógica para rechazar cookies no esenciales
            console.log('Cookies rechazadas');
            window.location.hash = '';
        });
    }
});