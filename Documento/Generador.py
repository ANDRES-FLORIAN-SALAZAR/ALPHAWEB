import random
import os

def limpiar_pantalla():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    # Para Unix (Linux, macOS)
    else:
        os.system('clear')

# Función para crear un número aleatorio
def crear_numero():
    return str(random.randint(0, 9))

# Función para crear una letra minúscula aleatoria
def crear_letra_minuscula():
    letras = "abcdefghijklmnopqrstuvwxyz"
    i = random.randint(0, (len(letras)-1))
    return letras[i]

# Función para crear una letra mayúscula aleatoria
def crear_letra_mayuscula():
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i = random.randint(0, (len(letras)-1))
    return letras[i]

# Función para crear un símbolo aleatorio
def crear_simbolo():
    simbolos = "!@#$%&/()=?¡¿*`^[]+´´¨¨¨{}Ç,;:.-_"
    i = random.randint(0, (len(simbolos)-1))
    return simbolos[i]

# Función para crear una contraseña con especificaciones
def crear_contraseña(char_length, min_nums, min_minus, min_mayus, min_simbolos):
    
    # Verifica si la suma de los caracteres no exceda el limite establecido
    if min_nums + min_minus + min_mayus + min_simbolos > char_length:
        print("Los valores que ingresaste no son válidos, intenta nuevamente.")
        return None

    password = []
    # Genera la contraseña según las especificaciones
    while len(password) < char_length:
        if min_nums > 0:
            password.append(crear_numero())
            min_nums -= 1
        if min_minus > 0 and len(password) < char_length:
            password.append(crear_letra_minuscula())
            min_minus -= 1
        if min_mayus > 0 and len(password) < char_length:
            password.append(crear_letra_mayuscula())
            min_mayus -= 1
        if min_simbolos > 0 and len(password) < char_length:
            password.append(crear_simbolo())
            min_simbolos -= 1
            
        # Completa la contraseña con caracteres aleatorios dentro del limite ya especificado
        while len(password) < char_length:
            functions = [crear_numero, crear_letra_minuscula, crear_letra_mayuscula, crear_simbolo]
            password.append(functions[random.randint(0, len(functions)-1)]())
    
    random.shuffle(password)
    return ''.join(password)



