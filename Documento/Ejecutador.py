from Menú import mostrar_menu, ver_instrucciones, crear_contraseña_personalizada, crear_contraseña_aleatoria
from Generador import limpiar_pantalla

# Función principal que controla el flujo del programa
def main():
    while True:
        limpiar_pantalla() # Limpia la pantalla cada vez que se cumple el ciclo
        mostrar_menu() # Opción de mostrar el menú de inicio
        opcion = input("Selecciona una opción: ") 

        if opcion == "1":
            crear_contraseña_personalizada() # Crea la contraseña especifica con los parametros establecidos
        elif opcion == "2":
            crear_contraseña_aleatoria() # Crea la contraseña aleatoria dependiendo la cantidad de caracteres escogidos
        elif opcion == "3":
            ver_instrucciones() # Muestra las instrucciones
            input("Presiona Enter para continuar...")
        elif opcion == "4":
            print("Saliendo del programa.")
            return main # Finaliza el programa
        else:
            print("Opción no válida. Intenta de nuevo.")
            input("Presiona Enter para continuar...")
        
if __name__ == "__main__":
    main() # Ejecuta la función de inicio del Programa
