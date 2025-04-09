from Generador import limpiar_pantalla, crear_contraseña

# Función para mostrar el menú principal
def mostrar_menu():
    print("Bienvenido al generador de contraseñas")
    print("1. Crear contraseña personalizada")
    print("2. Crear contraseña aleatoria")
    print("3. Ver instrucciones")
    print("4. Salir")

# Función para mostrar las instrucciones
def ver_instrucciones():
    print("Instrucciones:")
    print("1. Selecciona 'Crear contraseña personalizada' para generar una contraseña especificando la cantidad de números,letras minúsculas, mayúsculas y símbolos.")
    print("2. Selecciona 'Crear contraseña aleatoria' para generar una contraseña sin especificaciones.")
    print("3. Sigue las indicaciones en pantalla para personalizar tu contraseña.")
    print("4. Selecciona 'Salir' para terminar el programa.")

# Función para crear una contraseña personalizada
def crear_contraseña_personalizada():
    characters = int(input("El número máximo de caracteres es 20: "))
    minimo_numeros = int(input("Cuántos números quieres: "))
    minimo_letra_minuscula = int(input("Cuántas letras minúsculas quieres: "))
    minimo_letra_mayuscula = int(input("Cuántas letras mayúsculas quieres: "))
    minimo_simbolo = int(input("Cuántos símbolos quieres: "))
    final_password = crear_contraseña(characters, minimo_numeros, minimo_letra_minuscula, minimo_letra_mayuscula, minimo_simbolo)
    if final_password:
        print(f"Tu contraseña es: {final_password}")
    else:
        print("Por favor, intenta de nuevo con valores válidos.")
    input("Presiona Enter para continuar...")
    
# Función para crear una contraseña aleatoria
def crear_contraseña_aleatoria():
    characters = int(input("El número máximo de caracteres es 20: "))
    final_password = crear_contraseña(characters, characters//4, characters//4, characters//4, characters//4)# Valida la cantidad de varibles que se creo
    if final_password:
        print(f"Tu contraseña es: {final_password}")
    else:
        print("Por favor, intenta de nuevo con valores válidos.")
    input("Presiona Enter para continuar...")
