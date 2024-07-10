from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def navegar_al_proyecto(driver):
    # Hacer click en la pestaña "Peticiones"
    try:
        peticiones_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Peticiones")]'))
        )
        peticiones_tab.click()
        print("Clickear en 'Peticiones' tab")
    except Exception as e:
        print(f"Error al clickear en 'Peticiones' tab: {e}")
        return

    # Esperar a que cargue la página
    time.sleep(2)

    # Seleccionar el dropdown de proyectos "Ir al proyecto..."
    try:
        proyecto_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="drdn-trigger" and contains(text(), "Ir al proyecto...")]'))
        )
        proyecto_dropdown.click()
        print("Clickear en ...ir a proyectos")
    except Exception as e:
        print(f"Error filtrando búsqueda en ...ir a proyectos: {e}")
        return

    time.sleep(1)

    # Seleccionar el proyecto "BAC - Soporte Infraestructura"
    try:
        proyecto = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="drdn-content"]//a[contains(@title, "BAC -Soporte Infraestructura")]'))
        )
        proyecto.click()
        print("Seleccionar 'BAC - Soporte Infraestructura'")
    except Exception as e:
        print(f"Error seleccionando proyecto: {e}")
        return

    # Esperar a que cargue la página del proyecto
    time.sleep(3)
