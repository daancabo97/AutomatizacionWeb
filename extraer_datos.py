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
            print("Visualizacion de incidencias encontradas en la tabla")
        except Exception as e:
            print(f"Error al encontrar incidencias en la tabla: {e}")
            break
        
        rows = table.find_elements(By.XPATH, './/tbody/tr')
        for row in rows:
            columns = row.find_elements(By.XPATH, './/td')
            if len(columns) == 8:  # Asegurarse de que haya exactamente 8 columnas
               if "BAC InfraNoProd" in columns[6].text:
                    datos.append({
                        '#': columns[0].text,
                        'Proyecto': columns[1].text,
                        'Tipo': columns[2].text,
                        'Estado': columns[3].text,
                        'Prioridad': columns[4].text,
                        'Asunto': columns[5].text,
                        'Asignado a': columns[6].text,
                        'Actualizado': columns[7].text
                    })
        print(f"Informacion capturada de: {len(datos)}")

        # Verificar si hay una segunda página
        try:
            siguiente_pagina = driver.find_element(By.XPATH, '//a[@rel="next"]')
            siguiente_pagina.click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]//tbody/tr'))
            )
            print("Redirecionando a siguiente pagina")
        except:
            print("No hay mas paginas encontradas, error de navegacion")
            break
    
    return datos