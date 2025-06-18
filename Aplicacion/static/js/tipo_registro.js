// Manejo de tipos de registro
function mostrarCampos() {
    const tipoRegistro = document.getElementById("tipo_registro").value;
    
    // Ocultar ambos formularios primero
    document.getElementById("campos_natural").style.display = "none";
    document.getElementById("campos_empresa").style.display = "none";
    
    // Mostrar el formulario correspondiente
    if (tipoRegistro === "natural") {
        document.getElementById("campos_natural").style.display = "block";
    } else if (tipoRegistro === "empresa") {
        document.getElementById("campos_empresa").style.display = "block";
    }
}

// Asegurar que se ejecute cuando cambie el select y cuando se cargue la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarCampos(); // Ejecutar al cargar la página
    
    // Ejecutar cuando cambie el select de tipo de registro
    document.getElementById("tipo_registro").addEventListener("change", mostrarCampos);
});
