"""
Script de Selenium para automatizar el registro e inicio de sesión
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys
import datetime

def generar_datos_unicos():
    """Genera datos únicos para cada prueba basados en el timestamp actual"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "nombre": "Test",
        "apellido": f"Usuario{timestamp[-6:]}",  # Usa los últimos 6 dígitos del timestamp
        "email": f"test.usuario{timestamp}@gmail.com",
        "contrasena": "Test123!" + timestamp[-4:],  # Agrega los últimos 4 dígitos
        "confirmar_contrasena": "Test123!" + timestamp[-4:],
        "edad": "28",
        "telefono": "310" + timestamp[-7:],  # Usa los últimos 7 dígitos
        "genero": "Masculino"
    }

def setup_driver():
    """Configura y retorna el driver de Chrome con opciones optimizadas"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        print(f"Error al inicializar el driver: {e}")
        sys.exit(1)

def wait_and_click(driver, by, value, timeout=10, description="elemento"):
    """Espera a que un elemento sea clickeable y hace clic en él"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        print(f"✓ Clic exitoso en {description}")
        return True
    except TimeoutException:
        print(f"✗ Timeout: No se pudo hacer clic en {description}")
        return False
    except Exception as e:
        print(f"✗ Error al hacer clic en {description}: {e}")
        return False

def wait_and_send_keys(driver, by, value, text, timeout=10, description="campo"):
    """Espera a que un elemento sea visible y envía texto"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        element.clear()
        element.send_keys(text)
        print(f"✓ Texto enviado a {description}: {text}")
        return True
    except TimeoutException:
        print(f"✗ Timeout: No se pudo encontrar {description}")
        return False
    except Exception as e:
        print(f"✗ Error al enviar texto a {description}: {e}")
        return False

def main():
    print("Iniciando automatización de registro e inicio de sesión...")
    
    # Inicialización del navegador
    driver = setup_driver()
    
    try:
        # Navegar a la página de registro
        print("Navegando a la página de registro...")
        driver.get("http://127.0.0.1:8000/registro/")
        driver.maximize_window()
        
        # Esperar a que la página cargue completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Seleccionar tipo de registro
        print("Seleccionando tipo de registro...")
        if wait_and_click(driver, By.NAME, "tipo_registro", description="selector de tipo"):
            time.sleep(1)
            wait_and_click(driver, By.XPATH, "//option[@value='natural']", description="opción natural")
        
        # Esperar a que se muestren los campos de persona natural
        time.sleep(2)
        
        # Generar datos únicos para esta prueba
        datos_unicos = generar_datos_unicos()
        
        # Datos de registro usando los datos únicos
        datos_registro = [
            ("nombre", datos_unicos["nombre"]),
            ("apellido", datos_unicos["apellido"]),
            ("email", datos_unicos["email"]),
            ("contrasena", datos_unicos["contrasena"]),
            ("confirmar_contrasena", datos_unicos["confirmar_contrasena"]),
            ("edad", datos_unicos["edad"]),
            ("telefono", datos_unicos["telefono"]),
            ("genero", datos_unicos["genero"])
        ]
        
        # Llenar formulario de registro
        print("Llenando formulario de registro...")
        for campo, valor in datos_registro:
            if campo == "genero":
                # Para el select de género
                if wait_and_click(driver, By.NAME, "genero", description="selector de género"):
                    time.sleep(1)
                    wait_and_click(driver, By.XPATH, f"//option[@value='{valor}']", description=f"opción {valor}")
            else:
                # Para los demás campos
                wait_and_send_keys(driver, By.NAME, campo, valor, description=campo)
            time.sleep(1)
        
        # Enviar formulario de registro
        print("Enviando formulario de registro...")
        if wait_and_click(driver, By.CSS_SELECTOR, "button[type='submit']", description="botón de registro"):
            time.sleep(3)
            print("✓ Registro completado")
        
        # Esperar un momento antes de iniciar sesión
        time.sleep(3)
        
        # Iniciar sesión
        print("Iniciando sesión...")
        
        # Buscar el enlace de inicio de sesión
        try:
            # Intentar con selector más específico
            enlace_login = driver.find_element(By.XPATH, "//h1/a[contains(text(), 'Inicia sesión aquí')]")
            enlace_login.click()
            print("✓ Enlace de inicio de sesión encontrado y clickeado")
            time.sleep(3)
        except Exception as e:
            print(f"✗ Error al encontrar/clickear enlace de inicio de sesión: {e}")
            return False
            
        # Datos de inicio de sesión usando los datos únicos
        datos_login = {
            "email": datos_unicos["email"],
            "contrasena": datos_unicos["contrasena"]
        }
        
        # Llenar formulario de inicio de sesión
        print("Llenando formulario de inicio de sesión...")
        for campo, valor in datos_login.items():
            try:
                # Esperar a que el campo sea visible
                elemento = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME, campo))
                )
                elemento.clear()
                elemento.send_keys(valor)
                print(f"✓ Llenado de campo {campo} exitoso")
                time.sleep(1)
            except Exception as e:
                print(f"✗ Error al llenar campo {campo}: {e}")
                return False
        
        # Enviar formulario de inicio de sesión
        print("Enviando formulario de inicio de sesión...")
        try:
            # Intentar con diferentes selectores para el botón
            botones = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Iniciar sesión')]")
            ]
            
            for by, selector in botones:
                try:
                    boton = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    boton.click()
                    print("✓ Botón de inicio de sesión encontrado y clickeado")
                    time.sleep(3)
                    break
                except Exception:
                    continue
        except Exception as e:
            print(f"✗ Error al enviar formulario de inicio de sesión: {e}")
            return False
        
        print("✓ Proceso completo exitosamente")
        return True
        
    except Exception as e:
        print(f"✗ Error durante la ejecución: {e}")
        return False
        
    finally:
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)