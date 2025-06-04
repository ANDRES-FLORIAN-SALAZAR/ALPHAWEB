
function crearNumero() {
    return String.fromCharCode(Math.floor(Math.random() * 10) + 48);
}

function crearLetraMinuscula() {
    return String.fromCharCode(Math.floor(Math.random() * 26) + 97);
}

function crearLetraMayuscula() {
    return String.fromCharCode(Math.floor(Math.random() * 26) + 65);
}

function crearSimbolo() {
    const simbolos = "!@#$%^&*()_+[]{}|;:,.<>?";
    return simbolos[Math.floor(Math.random() * simbolos.length)];
}

function actualizarCampos() {
    const charLength = parseInt(document.querySelector('input[name="char_length"]').value);
    const maxNums = Math.floor(charLength * 0.2);
    const maxMinus = Math.floor(charLength * 0.3);
    const maxMayus = Math.floor(charLength * 0.3);
    const maxSimbolos = Math.floor(charLength * 0.2);

    document.querySelector('input[name="min_nums"]').max = maxNums;
    document.querySelector('input[name="min_minus"]').max = maxMinus;
    document.querySelector('input[name="min_mayus"]').max = maxMayus;
    document.querySelector('input[name="min_simbolos"]').max = maxSimbolos;
}

function generarContrasena() {
    const charLength = parseInt(document.querySelector('input[name="char_length"]').value);
    let minNums = parseInt(document.querySelector('input[name="min_nums"]').value);
    let minMinus = parseInt(document.querySelector('input[name="min_minus"]').value);
    let minMayus = parseInt(document.querySelector('input[name="min_mayus"]').value);
    let minSimbolos = parseInt(document.querySelector('input[name="min_simbolos"]').value);

    let password = [];

    while (password.length < charLength) {
        if (minNums > 0) {
            password.push(crearNumero());
            minNums--;
        }
        if (minMinus > 0 && password.length < charLength) {
            password.push(crearLetraMinuscula());
            minMinus--;
        }
        if (minMayus > 0 && password.length < charLength) {
            password.push(crearLetraMayuscula());
            minMayus--;
        }
        if (minSimbolos > 0 && password.length < charLength) {
            password.push(crearSimbolo());
            minSimbolos--;
        }

        while (password.length < charLength) {
            const functions = [crearNumero, crearLetraMinuscula, crearLetraMayuscula, crearSimbolo];
            password.push(functions[Math.floor(Math.random() * functions.length)]());
        }
    }

    document.querySelector('input[name="contrasena"]').value = password.join('');
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('input[name="char_length"]').addEventListener('input', actualizarCampos);
});
