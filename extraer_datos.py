from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def extraer_datos(driver):
    datos = []

    while True:
        # Esperar a que la tabla cargue
        try:
            table = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]'))
            )
            print("Visualización de incidencias encontradas en la tabla")
        except Exception as e:
            print(f"Error al encontrar incidencias en la tabla: {e}")
            break

        rows = table.find_elements(By.XPATH, './/tbody/tr')
        for row in rows:
            columns = row.find_elements(By.XPATH, './/td')
            if len(columns) >= 8:  # Asegurarse de que haya al menos 8 columnas
                if "BAC InfraNoProd" in columns[7].text:
                    datos.append({
                        '#': columns[1].text,
                        'Proyecto': columns[2].text,
                        'Tipo': columns[3].text,
                        'Estado': columns[4].text,
                        'Prioridad': columns[5].text,
                        'Asunto': columns[6].text,
                        'Asignado a': columns[7].text,
                        'Actualizado': columns[8].text
                    })

        print(f"Información capturada de: {len(datos)} elementos")

        # Verificar si hay una segunda página
        try:
            siguiente_pagina = driver.find_element(By.XPATH, '//a[@rel="next"]')
            siguiente_pagina.click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]//tbody/tr'))
            )
            print("Redireccionando a la siguiente página")
        except:
            print("No hay más casos de 'BAC InfraNoProd' en las siguientes páginas")
            break

    if datos:
        # Crear DataFrame y exportar a Excel
        df = pd.DataFrame(datos)
        df.to_excel('reporte.xlsx', index=False)
        print("Datos extraídos y guardados en reporte.xlsx")
    else:
        print("No se ha extraído información")
    
    return datos
