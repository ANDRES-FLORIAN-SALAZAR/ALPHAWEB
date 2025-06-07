"""
Inspector de elementos web para Selenium.

Este script navega a una página web y muestra información sobre los elementos
presentes en la página, incluyendo enlaces, botones y mensajes.
"""

import sys
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


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

    Esta función navega a la página de registro y muestra información
    sobre los elementos presentes en la página.
    """
    try:
        # Iniciar el navegador
        driver = setup_driver()
        driver.get("http://127.0.0.1:8000/registro/")

        # Esperar a que la página cargue
        time.sleep(5)

        # Imprimir todos los enlaces disponibles
        print("\nEnlaces encontrados:")
        enlaces = driver.find_elements(By.TAG_NAME, "a")
        for i, enlace in enumerate(enlaces, 1):
            print(f"Enlace {i}:")
            print(f"  Texto: {enlace.text}")
            print(f"  Clase: {enlace.get_attribute('class')}")
            print(f"  Href: {enlace.get_attribute('href')}")
            print("-" * 50)

        # Imprimir todos los botones disponibles
        print("\nBotones encontrados:")
        botones = driver.find_elements(By.TAG_NAME, "button")
        for i, boton in enumerate(botones, 1):
            print(f"Botón {i}:")
            print(f"  Texto: {boton.text}")
            print(f"  Clase: {boton.get_attribute('class')}")
            print(f"  Tipo: {boton.get_attribute('type')}")
            print("-" * 50)

        # Esperar a que aparezcan los mensajes
        if not WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, ".alert")),
        ):
            print("No se encontraron mensajes en la página")
            return

        mensajes = driver.find_elements(By.CSS_SELECTOR, ".alert")
        print("\nMensajes encontrados:")
        for i, mensaje in enumerate(mensajes, 1):
            print(f"Mensaje {i}:")
            print(f"  Texto: {mensaje.text}")
            print(f"  Clase: {mensaje.get_attribute('class')}")
            print("-" * 50)

    except WebDriverException as e:
        print(f"Error durante la inspección: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
