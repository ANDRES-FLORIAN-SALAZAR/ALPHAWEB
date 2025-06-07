"""Este modulo recrea la automatización del proyecto."""
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime

from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotVisibleException, NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def generar_datos_unicos() -> dict[str, str]:
    """Genera datos únicos para cada prueba basados en el timestamp actual."""
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    return {
        "nombre": "Test",
        "apellido": f"Usuario{timestamp[-6:]}",
        "email": f"test.usuario{timestamp}@gmail.com",
        "contrasena": "Test123!" + timestamp[-4:],
        "confirmar_contrasena": "Test123!" + timestamp[-4:],
        "edad": "28",
        "telefono": "310" + timestamp[-7:],
        "genero": "Masculino",
    }

def setup_driver() -> WebDriver:
    """
    Configura y retorna el driver de Chrome con opciones optimizadas.

    Returns:
        WebDriver: El controlador de Selenium configurado.

    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        })
    except WebDriverException as e:
        print(f"Error crítico al configurar el driver: {e}")
        sys.exit(1)
    else:
        return driver
    finally:
        pass  # Asegurar que el bloque try tenga un finally

def wait_and_click(
    driver: WebDriver,
    by: By,
    value: str,
    timeout: int = 10,
    description: str = "elemento",
) -> bool:
    """Espera a que un elemento sea clickeable y hace clic en él."""
    try:
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.element_to_be_clickable((by, value)),
        )
        element.click()
    except TimeoutException:
        print(f"✗ Timeout: No se pudo hacer clic en {description}")
        return False
    except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
        print(f"✗ Error al hacer clic en {description}: {e}")
        return False
    else:
        print(f"✓ Clic exitoso en {description}")
        return True

@dataclass
class InputLocator:
    """

    Clase para definir un localizador de entrada de texto.

    Esta clase encapsula los detalles necesarios para localizar un campo de entrada
    y enviarle texto de manera segura y eficiente.
    """

    driver: WebDriver
    by: By
    value: str
    text: str
    timeout: int = 10
    description: str = "campo"

def wait_and_send_keys(
    driver: WebDriver,
    by: str,
    value: str,
    text: str,
    timeout: int = 10,
    description: str = "campo",
) -> bool:
    """Espera a que un elemento sea visible y envía texto."""
    try:
        element = WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located((by, value)),
        )
        element.clear()
        element.send_keys(text)
    except TimeoutException:
        print(f"✗ Timeout: No se pudo encontrar {description}")
        return False
    except (ElementNotInteractableException, ElementNotVisibleException) as e:
        print(f"✗ Error al interactuar con {description}: {e}")
        return False
    else:
        print(f"✓ Texto enviado a {description}: {text}")
        return True

def navegar_a_registro(driver: WebDriver) -> bool:
    """
    Navega a la página de registro.

    Args:
        driver (WebDriver): El controlador de Selenium.

    Returns:
        bool: True si la navegación fue exitosa, False en caso contrario.

    """
    try:
        driver.get("http://127.0.0.1:8000/registro/")
        driver.maximize_window()
        WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.TAG_NAME, "body")),
        )
    except (TimeoutException, WebDriverException) as e:
        print(f"✗ Error al navegar a registro: {e}")
        return False
    else:
        return True

def llenar_formulario_registro(driver: WebDriver, datos: dict[str, str]) -> bool:
    """
    Llena el formulario de registro con los datos proporcionados.

    Args:
        driver (WebDriver): El controlador de Selenium.
        datos (dict[str, str]): Un diccionario con los datos del formulario.

    Returns:
        bool: True si el formulario se llenó correctamente, False en caso contrario.

    """
    for campo, valor in datos.items():
        if campo == "genero":
            if wait_and_click(driver, By.NAME, "genero", description="selector de género"):
                time.sleep(1)
                wait_and_click(driver, By.XPATH, f"//option[@value='{valor}']", description=f"opción {valor}")
        else:
            wait_and_send_keys(driver, By.NAME, campo, valor, description=campo)
        time.sleep(1)
    return True

def iniciar_sesion(driver: WebDriver, datos: dict[str, str]) -> bool:
    """
    Inicia sesión en la aplicación.

    Args:
        driver (WebDriver): El controlador de Selenium.
        datos (dict[str, str]): Un diccionario con los datos de inicio de sesión.

    Returns:
        bool: True si el inicio de sesión fue exitoso, False en caso contrario.

    Raises:
        WebDriverException: Si hay un error crítico durante el inicio de sesión.

    """
    try:
        print("Navegando a la página de inicio de sesión...")
        driver.get("http://127.0.0.1:8000/inicio-sesion/")
        time.sleep(3)

        # Verificar que la página cargó correctamente usando múltiples selectores
        print("Verificando que la página cargó correctamente...")
        try:
            # Intentar con nombre del campo email
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.NAME, "email")),
            )
            print("✓ Página de inicio de sesión cargada correctamente")
        except TimeoutException:
            try:
                # Intentar con ID
                WebDriverWait(driver, 5).until(
                    expected_conditions.presence_of_element_located((By.ID, "email")),
                )
                print("✓ Página de inicio de sesión cargada correctamente")
            except TimeoutException:
                try:
                    # Intentar con CSS
                    WebDriverWait(driver, 5).until(
                        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']")),
                    )
                    print("✓ Página de inicio de sesión cargada correctamente")
                except TimeoutException:
                    print("✗ Error: No se cargó la página de inicio de sesión correctamente")
                    return False

        # Llenar el formulario
        print("Llenando formulario de inicio de sesión...")
        for campo, valor in datos.items():
            print(f"Llenando campo: {campo}")
            try:
                # Intentar con nombre del campo
                elemento = WebDriverWait(driver, 5).until(
                    expected_conditions.element_to_be_clickable((By.NAME, campo)),
                )
                print(f"✓ Encontrado campo {campo} por nombre")
            except TimeoutException:
                try:
                    # Intentar con ID
                    elemento = WebDriverWait(driver, 5).until(
                        expected_conditions.element_to_be_clickable((By.ID, campo)),
                    )
                    print(f"✓ Encontrado campo {campo} por ID")
                except TimeoutException:
                    try:
                        # Intentar con CSS
                        elemento = WebDriverWait(driver, 5).until(
                            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, f"input[name='{campo}']")),
                        )
                        print(f"✓ Encontrado campo {campo} por CSS")
                    except TimeoutException:
                        print(f"✗ Error: No se pudo encontrar el campo {campo}")
                        return False

            try:
                elemento.clear()
                elemento.send_keys(valor)
                print(f"✓ Llenado de campo {campo} exitoso")
            except (ElementNotInteractableException, WebDriverException) as e:
                print(f"✗ Error al llenar campo {campo}: {e}")
                return False

        # Enviar el formulario
        print("Enviando formulario de inicio de sesión...")
        if not enviar_formulario_login(driver):
            print("✗ Error al enviar el formulario de inicio de sesión")
            return False

        # Verificar si se inició sesión exitosamente
        print("Verificando inicio de sesión exitoso...")
        try:
            # Verificar dashboard
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".dashboard, .menu-principal, .user-info")),
            )
            print("✓ Inicio de sesión exitoso confirmado")
            return True
        except TimeoutException:
            # Verificar mensajes de error
            try:
                mensaje_error = WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .error, .mensaje-error")),
                )
                print(f"✗ Mensaje de error: {mensaje_error.text}")
                return False
            except TimeoutException:
                # Si no hay error y no se encuentra dashboard, verificar si hay mensaje de éxito
                try:
                    mensaje_exito = WebDriverWait(driver, 3).until(
                        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert-success, .success, .mensaje-exito")),
                    )
                    print(f"✓ Mensaje de éxito encontrado: {mensaje_exito.text}")
                    return True
                except TimeoutException:
                    print("✗ Error: No se pudo confirmar el inicio de sesión exitoso")
                    return False

    except WebDriverException as e:
        print(f"✗ Error durante el inicio de sesión: {e}")
        return False

def enviar_formulario_login(driver: WebDriver) -> bool:
    """
    Envía el formulario de inicio de sesión.

    Args:
        driver (WebDriver): El controlador de Selenium.

    Returns:
        bool: True si el envío fue exitoso, False en caso contrario.

    Raises:
        WebDriverException: Si hay un error crítico durante el envío.

    """
    try:
        # Buscar botón de inicio de sesión usando múltiples selectores
        print("Buscando botón de inicio de sesión...")
        boton = None

        # Intentar con XPATH con diferentes textos
        for texto in ["Iniciar Sesión", "Iniciar sesión", "Login", "login", "Entrar", "Ingresar", "Ingresar Sesión"]:
            try:
                boton = WebDriverWait(driver, 3).until(
                    expected_conditions.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{texto}')]")),
                )
                print(f"✓ Botón encontrado con XPATH usando texto: {texto}")
                break
            except TimeoutException:
                continue

        # Si no se encontró con XPATH, intentar con CSS
        if boton is None:
            for selector in [
                "button[type='submit']",
                "input[type='submit']",
                "button.btn-primary",
                "button.btn-success",
                "button.btn",
                "button[type='button']",
                "input[type='button']",
            ]:
                try:
                    boton = WebDriverWait(driver, 3).until(
                        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, selector)),
                    )
                    print(f"✓ Botón encontrado con CSS usando selector: {selector}")
                    break
                except TimeoutException:
                    continue

        # Si no se encontró con CSS, intentar con nombre
        if boton is None:
            for nombre in ["iniciar_sesion", "login", "entrar", "submit", "ingresar"]:
                try:
                    boton = WebDriverWait(driver, 3).until(
                        expected_conditions.element_to_be_clickable((By.NAME, nombre)),
                    )
                    print(f"✓ Botón encontrado con nombre: {nombre}")
                    break
                except TimeoutException:
                    continue

        # Si no se encontró con nombre, intentar con ID
        if boton is None:
            for id in ["iniciar-sesion", "login", "entrar", "submit", "ingresar", "btn-login", "btn-iniciar-sesion"]:
                try:
                    boton = WebDriverWait(driver, 3).until(
                        expected_conditions.element_to_be_clickable((By.ID, id)),
                    )
                    print(f"✓ Botón encontrado con ID: {id}")
                    break
                except TimeoutException:
                    continue

        if boton is None:
            print("✗ No se pudo encontrar el botón de inicio de sesión")
            return False

        # Intentar varios métodos de clic
        print("Intentando hacer clic en el botón...")
        try:
            # Método 1: Clic normal
            boton.click()
            print("✓ Botón clickeado con método normal")
        except ElementClickInterceptedException:
            # Método 2: Clic usando JavaScript
            driver.execute_script("arguments[0].click();", boton)
            print("✓ Botón clickeado con JavaScript")
        except WebDriverException as e:
            print(f"✗ Error al clickear el botón: {e}")
            return False

        # Esperar a que la página cargue después del clic
        print("Esperando que la página cargue...")
        time.sleep(3)

        # Verificar si hay algún mensaje de error
        print("Verificando mensajes de error...")
        try:
            mensaje_error = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .error, .mensaje-error")),
            )
            print(f"✗ Mensaje de error encontrado: {mensaje_error.text}")
            return False
        except TimeoutException:
            print("✓ No se encontró mensaje de error")

        # Verificar si hay algún mensaje de éxito
        print("Verificando mensajes de éxito...")
        try:
            mensaje_exito = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert-success, .success, .mensaje-exito")),
            )
            print(f"✓ Mensaje de éxito encontrado: {mensaje_exito.text}")
            return True
        except TimeoutException:
            print("✓ No se encontró mensaje de éxito")

        # Verificar si se redirigió a la página de dashboard
        print("Verificando redirección a dashboard...")
        try:
            WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".dashboard, .menu-principal, .user-info")),
            )
            print("✓ Redirección exitosa al dashboard")
            return True
        except TimeoutException:
            print("✓ No se encontró dashboard, asumiendo éxito")
            return True

    except WebDriverException as e:
        print(f"✗ Error al enviar formulario: {e}")
        return False


def seleccionar_tipo_registro(driver: WebDriver) -> bool:
    """
    Selecciona el tipo de registro y el tipo de usuario.

    Args:
        driver (WebDriver): El controlador de Selenium.

    Returns:
        bool: True si la selección fue exitosa, False en caso contrario.

    """
    try:
        # Seleccionar tipo de registro
        if not wait_and_click(driver, By.NAME, "tipo_registro", description="selector de tipo"):
            return False
        time.sleep(1)

        # Seleccionar tipo de usuario
        if not wait_and_click(driver, By.XPATH, "//option[@value='natural']", description="opción natural"):
            return False

        return True
    except WebDriverException as e:
        print(f"✗ Error al seleccionar tipo de registro: {e}")
        return False

def enviar_formulario_registro(driver: WebDriver) -> bool:
    """
    Envía el formulario de registro.

    Args:
        driver (WebDriver): El controlador de Selenium.

    Returns:
        bool: True si el envío fue exitoso, False en caso contrario.

    """
    try:
        # Buscar botón de registro
        boton_registro = WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Registrarse')]")),
        )
        print("✓ Botón de registro encontrado")

        # Intentar hacer scroll hasta el botón
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", boton_registro)
            time.sleep(0.5)
        except WebDriverException as e:
            print(f"✗ Error al hacer scroll: {e}")

        # Intentar varios métodos de clic
        try:
            # Método 1: Clic normal
            boton_registro.click()
            print("✓ Botón de registro clickeado con método normal")
        except ElementClickInterceptedException:
            # Método 2: Clic usando JavaScript
            driver.execute_script("arguments[0].click();", boton_registro)
            print("✓ Botón de registro clickeado con JavaScript")
        except WebDriverException as e:
            print(f"✗ Error al clickear el botón: {e}")
            return False

        # Esperar a que la página cargue después del clic
        time.sleep(3)

        # Verificar si hay algún mensaje de error
        try:
            mensaje_error = WebDriverWait(driver, 3).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger")),
            )
            print(f"✗ Mensaje de error encontrado: {mensaje_error.text}")
        except TimeoutException:
            print("✓ No se encontró mensaje de error, asumiendo éxito")
        else:
            return False

        return True

    except WebDriverException as e:
        print(f"✗ Error al enviar formulario de registro: {e}")
        return False

def registrar_usuario(driver: WebDriver, datos: dict[str, str]) -> bool:
    """
    Realiza el registro de un nuevo usuario.

    Args:
        driver (WebDriver): El controlador de Selenium.
        datos (dict[str, str]): Datos del usuario a registrar.

    Returns:
        bool: True si el registro fue exitoso, False en caso contrario.

    """
    success = False
    try:
        # Seleccionar tipo de registro
        if not seleccionar_tipo_registro(driver):
            return False

        # Llenar formulario de registro
        if not llenar_formulario_registro(driver, datos):
            return False

        # Enviar formulario de registro
        if not enviar_formulario_registro(driver):
            return False

        success = True

    except WebDriverException as e:
        print(f"✗ Error durante el registro: {e}")
    return success

def ejecutar_prueba(driver: WebDriver) -> bool:
    """
    Ejecuta la prueba completa de registro e inicio de sesión.

    Args:
        driver (WebDriver): El controlador de Selenium.

    Returns:
        bool: True si la prueba fue exitosa, False en caso contrario.

    """
    success = False
    try:
        # Generar datos únicos
        datos = generar_datos_unicos()
        print(f"✓ Datos generados: {datos}")

        # Navegar a registro
        max_intentos = 3
        for intento in range(max_intentos):
            print(f"Intento {intento + 1} de {max_intentos} para navegar a registro...")
            if navegar_a_registro(driver):
                print("✓ Navegación a registro exitosa")
                break
            print(f"✗ Intento {intento + 1} fallido, esperando 2 segundos antes de reintentar...")
            time.sleep(2)
        else:
            print("✗ Todos los intentos de navegación a registro fallaron")
            return False

        # Registrar usuario
        if not registrar_usuario(driver, datos):
            print("✗ Registro fallido")
            return False

        # Iniciar sesión
        print("\nIniciando proceso de inicio de sesión...")
        if iniciar_sesion(driver, {"email": datos["email"], "contrasena": datos["contrasena"]}):
            print("✓ Inicio de sesión exitoso")
        else:
            print("✗ Inicio de sesión fallido")
            return False

        success = True

    except WebDriverException as e:
        print(f"✗ Error durante la ejecución: {e}")
    return success

def main() -> bool:
    """
    Función principal para ejecutar la automatización de pruebas.

    Returns:
        bool: True si la ejecución fue exitosa, False en caso contrario.

    """
    print("Iniciando automatización de registro e inicio de sesión...")
    driver = setup_driver()
    try:
        return ejecutar_prueba(driver)
    except WebDriverException as e:
        print(f"✗ Error durante la ejecución: {e}")
        return False
    finally:
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
