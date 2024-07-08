from selenium.webdriver.common.by import By
import time

def extraer_datos(driver):
    datos = []
    
    while True:
        # Esperar a que la tabla cargue
        time.sleep(2)
        
        # Encontrar todas las filas en la tabla de peticiones
        filas = driver.find_elements(By.XPATH, '//table[@class="list issues"]/tbody/tr')
        
        for fila in filas:
            columnas = fila.find_elements(By.TAG_NAME, 'td')
            proyecto = columnas[1].text
            tipo = columnas[2].text
            estado = columnas[3].text
            prioridad = columnas[4].text
            asunto = columnas[5].text
            asignado_a = columnas[6].text
            actualizado = columnas[7].text
            
            datos.append({
                'Proyecto': proyecto,
                'Tipo': tipo,
                'Estado': estado,
                'Prioridad': prioridad,
                'Asunto': asunto,
                'Asignado a': asignado_a,
                'Actualizado': actualizado
            })
        
        # Verificar si hay una segunda página
        try:
            siguiente_pagina = driver.find_element(By.XPATH, '//a[@class="next_page"]')
            siguiente_pagina.click()
        except:
            break
    
    return datos
