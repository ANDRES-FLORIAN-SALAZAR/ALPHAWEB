"""
Inspector de elementos web para la página de inicio.

Este script navega a la página de inicio y muestra información sobre los elementos
presentes en la página, incluyendo enlaces, botones y mensajes.
"""

import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def setup_driver() -> webdriver.Chrome:
    """
    Configura y retorna el driver de Chrome con opciones optimizadas.

    Returns:
        webdriver.Chrome: El driver configurado y listo para usar.

    Raises:
        SystemExit: Si hay un error al iniciar el navegador.

    """
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    try:
        return webdriver.Chrome(options=options)
    except WebDriverException as e:
        print(f"Error al iniciar el navegador: {e}")
        sys.exit(1)


def main() -> None:
    """
    Función principal para ejecutar la inspección.

    Esta función navega a la página de inicio y muestra información
    sobre los elementos presentes en la página.
    """
    driver = setup_driver()
    try:
        # Navegar a la página de inicio
        driver.get("http://127.0.0.1:8000/")
        time.sleep(3)

        # Listar todos los enlaces
        print("\n=== ENLACES ===")
        enlaces = driver.find_elements(By.TAG_NAME, "a")
        for enlace in enlaces:
            print(f"Text: {enlace.text}")
            print(f"Href: {enlace.get_attribute('href')}")
            print("-" * 50)

        # Listar todos los botones
        print("\n=== BOTONES ===")
        botones = driver.find_elements(By.TAG_NAME, "button")
        for boton in botones:
            print(f"Text: {boton.text}")
            print(f"Class: {boton.get_attribute('class')}")
            print(f"Type: {boton.get_attribute('type')}")
            print("-" * 50)

        # Listar mensajes de éxito y error
        print("\n=== MENSAJES ===")
        mensajes = driver.find_elements(By.CSS_SELECTOR, ".alert")
        for mensaje in mensajes:
            print(f"Text: {mensaje.text}")
            print(f"Class: {mensaje.get_attribute('class')}")
            print("-" * 50)

    except WebDriverException as e:
        print(f"Error durante la inspección: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
