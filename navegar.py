from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def navegar_al_proyecto(driver):
    # Hacer click en la pestaña "Peticiones"
    try:
        peticiones_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Peticiones")]'))
        )
        peticiones_tab.click()
        print("Clicked on 'Peticiones' tab")
    except Exception as e:
        print(f"Error clicking on 'Peticiones' tab: {e}")
        return

    # Esperar a que cargue la página
    time.sleep(2)

    # Seleccionar el dropdown de proyectos "Ir al proyecto..."
    try:
        proyecto_dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="drdn-trigger" and contains(text(), "Ir al proyecto...")]'))
        )
        proyecto_dropdown.click()
        print("Clicked on project dropdown")
    except Exception as e:
        print(f"Error finding project dropdown: {e}")
        return

    time.sleep(1)

    # Seleccionar el proyecto "BAC - Soporte Infraestructura"
    try:
        proyecto = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@class="drdn-content"]//a[contains(@title, "BAC -Soporte Infraestructura")]'))
        )
        proyecto.click()
        print("Selected 'BAC - Soporte Infraestructura' project")
    except Exception as e:
        print(f"Error selecting project: {e}")
        return

    # Esperar a que cargue la página del proyecto
    time.sleep(3)

    # Extraer datos de la tabla
    try:
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]'))
        )
        print("Found issues table")
        
        rows = table.find_elements(By.XPATH, './/tbody/tr')
        data = []
        for row in rows:
            columns = row.find_elements(By.XPATH, './/td')
            data.append([col.text for col in columns])

        # Crear un DataFrame de pandas
        df = pd.DataFrame(data, columns=["#", "Proyecto", "Tipo", "Estado", "Prioridad", "Asunto", "Asignado a", "Actualizado"])

        # Guardar el DataFrame en un archivo Excel
        df.to_excel("output.xlsx", index=False)
        print("Data extracted and saved to output.xlsx")
    except Exception as e:
        print(f"Error extracting data from table: {e}")
        return