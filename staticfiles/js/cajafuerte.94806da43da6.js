
function filtrarPorCategoria() {
    const categoria = document.getElementById('categoria-filter').value;
    const documentos = document.querySelectorAll('.documento-card');
    
    documentos.forEach(function(doc) {
        if (categoria === 'todas' || doc.getAttribute('data-categoria') === categoria) {
            doc.style.display = 'flex';
        } else {
            doc.style.display = 'none';
        }
    });
}

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}
