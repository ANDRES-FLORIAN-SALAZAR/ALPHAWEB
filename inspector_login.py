"""
Inspector de elementos web para la página de inicio de sesión.

Este script navega a la página de inicio de sesión y muestra información sobre los
componentes del formulario, incluyendo campos, botones y mensajes.
"""

import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def inspeccionar_login() -> None:
    """
    Función principal para inspeccionar la página de inicio de sesión.

    Esta función navega a la página de inicio de sesión y muestra información
    sobre los campos del formulario, botones y mensajes disponibles.
    """
    # Configurar el driver
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        # Iniciar el navegador
        driver = webdriver.Chrome(options=options)
        driver.get("http://127.0.0.1:8000/inicio-sesion/")

        # Esperar a que la página cargue
        time.sleep(3)

        # Imprimir información de los campos del formulario
        print("\n=== CAMPOS DEL FORMULARIO ===")
        campos = driver.find_elements(By.CSS_SELECTOR, "input")
        for campo in campos:
            print(f"Nombre: {campo.get_attribute('name')}")
            print(f"Tipo: {campo.get_attribute('type')}")
            print(f"Clase: {campo.get_attribute('class')}")
            print("-" * 50)

        # Imprimir información de los botones
        print("\n=== BOTONES ===")
        botones = driver.find_elements(By.CSS_SELECTOR, "button")
        for boton in botones:
            print(f"Texto: {boton.text}")
            print(f"Clase: {boton.get_attribute('class')}")
            print(f"Tipo: {boton.get_attribute('type')}")
            print("-" * 50)

        # Imprimir mensajes de error
        print("\n=== MENSAJES ===")
        mensajes = driver.find_elements(By.CSS_SELECTOR, ".alert")
        for mensaje in mensajes:
            print(f"Texto: {mensaje.text}")
            print(f"Clase: {mensaje.get_attribute('class')}")
            print("-" * 50)

    except WebDriverException as e:
        print(f"Error durante la inspección: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    inspeccionar_login()
