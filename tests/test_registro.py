"""Test module for user registration functionality using Selenium."""  # noqa: INP001

from typing import Never

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_registro_usuario() -> None:
    """Test the user registration process using Selenium."""
    # Configurar Firefox
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Modo sin interfaz gráfica
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")

    # Especifica la ruta a GeckoDriver si no está en tu PATH
    service = Service()  # Usa esto solo si geckodriver está en tu PATH
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Ir a la página de registro
        driver.get("http://127.0.0.1:8001/registro/")

        # Esperar a que la página cargue
        wait = WebDriverWait(driver, 10)

        # Seleccionar tipo de registro (Persona Natural)
        tipo_registro = wait.until(EC.element_to_be_clickable((By.NAME, "tipo_usuario")))
        tipo_registro.send_keys("natural")

        # Esperar a que los campos de persona natural aparezcan
        wait.until(EC.presence_of_element_located((By.NAME, "nombre_completo")))

        # Llenar el formulario de persona natural
        nombre_completo = driver.find_element(By.NAME, "nombre_completo")
        nombre_completo.send_keys("Juan Perez")

        email = driver.find_element(By.NAME, "email")
        email.send_keys("juan.perez+test@gmail.com")  # Usar un email único

        password1 = driver.find_element(By.NAME, "password1")
        password1.send_keys("Test123!Test")

        password2 = driver.find_element(By.NAME, "password2")
        password2.send_keys("Test123!Test")
        # Verificar que las contraseñas coinciden
        class PasswordMismatchError(AssertionError):
            def __init__(self) -> None:
                super().__init__("Las contraseñas no coinciden")

        def contrasena_no_coincide() -> None:
            def do_raise() -> None:
                raise PasswordMismatchError  # noqa: TRY301
            do_raise()

        mensaje_contrasena = wait.until(EC.presence_of_element_located((By.ID, "mensaje-contraseña")))
        if "Las contraseñas coinciden" not in mensaje_contrasena.text:
            contrasena_no_coincide()
        mensaje_contrasena = driver.find_element(By.ID, "mensaje-contraseña")
        if "Las contraseñas coinciden" not in mensaje_contrasena.text:
            msg = "Las contraseñas no coinciden"
            raise AssertionError(msg)  # noqa: TRY301

        # Esperar a que el botón de registro esté habilitado
        boton_registrar = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))

        # Hacer clic en el botón de registro
        boton_registrar.click()

        # Esperar a que se redirija a la página de planes
        wait.until(EC.url_contains("/Planes/"))

        # Verificar que se redirigió correctamente
        if "Planes" not in driver.title:
            msg = '"Planes" no está en el título de la página'
            raise AssertionError(msg)  # noqa: TRY301

        # Verificar que el usuario está autenticado
        try:
            # Buscar algún elemento que solo aparece cuando se está logueado
            perfil_usuario = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "perfil-usuario")))
            def raise_perfil_no_visible() -> Never:
                msg = "El perfil de usuario no está visible después del registro"
                raise AssertionError(msg)  # noqa: TRY301
            if not perfil_usuario.is_displayed():
                raise_perfil_no_visible()
        except Exception:
            print("Error: No se encontró el perfil de usuario después del registro")
            raise

        print("Registro exitoso!")

    except Exception as e:
        print(f"Error en la prueba: {e!s}")
        raise
    finally:
        # Cerrar el navegador
        driver.quit()

if __name__ == "__main__":
    test_registro_usuario()
