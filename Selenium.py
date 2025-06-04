# selenium_flujos_django.py

"""
Este script automatiza los flujos del sistema web con Selenium. Incluye:
- Registro de usuario
- Inicio de sesión
- Navegación a secciones clave

Nota: Se recomienda ejecutar este script antes de ejecutar las pruebas
formales para asegurar que los flujos principales están funcionando.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Inicialización del navegador
driver = webdriver.Chrome()
driver.get("http://127.0.0.1:8000")
driver.maximize_window()
time.sleep(2)

# Registro de nuevo usuario
driver.find_element(By.LINK_TEXT, "Registro").click()
time.sleep(1)
driver.find_element(By.ID, "tipo_registro").click()
driver.find_element(By.XPATH, "//option[@value='natural']").click()
driver.find_element(By.NAME, "nombre_completo").send_keys("Usuario Selenium")
driver.find_element(By.NAME, "email").send_keys("flujo_prueba@example.com")
driver.find_element(By.NAME, "password").send_keys("Prueba123*")
driver.find_element(By.NAME, "edad").send_keys("28")
driver.find_element(By.NAME, "celular").send_keys("987654321")
driver.find_element(By.NAME, "genero").find_element(By.XPATH, "//option[@value='Femenino']").click()
driver.find_element(By.TAG_NAME, "button").click()
time.sleep(2)

# Inicio de sesión
driver.find_element(By.NAME, "email").send_keys("flujo_prueba@example.com")
driver.find_element(By.NAME, "contrasena").send_keys("Prueba123*")
driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
time.sleep(2)

# Navegar a sección de caja fuerte
driver.find_element(By.LINK_TEXT, "Mi Caja Fuerte Digital").click()
time.sleep(2)

# Navegar a generador de contraseñas
driver.find_element(By.LINK_TEXT, "Generador de Contraseña").click()
time.sleep(2)

# Finalizar sesión
driver.find_element(By.LINK_TEXT, "Cerrar Sesión").click()
time.sleep(2)

driver.quit()

print("Flujos ejecutados correctamente.")