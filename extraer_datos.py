from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extraer_datos(driver, filtros):
    datos = {filtro: [] for filtro in filtros}

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

        filas = table.find_elements(By.XPATH, './/tbody/tr')
        for fila in filas:
            columns = fila.find_elements(By.XPATH, './/td')
            if len(columns) >= 8:
                for filtro in filtros:
                    if filtro in columns[7].text:
                        datos[filtro].append({
                            '#': columns[1].text,
                            'Proyecto': columns[2].text,
                            'Tipo': columns[3].text,
                            'Estado': columns[4].text,
                            'Prioridad': columns[5].text,
                            'Asunto': columns[6].text,
                            'Asignado a': columns[7].text,
                            'Actualizado': columns[8].text
                        })
                        break

        # Notificación de casos capturados para cada filtro
        for filtro in filtros:
            num_casos = len(datos[filtro])
            if num_casos > 0:
                notificacion(driver, f"Se han capturado: {num_casos} casos asignados a {filtro}", "info", time_out=10000)
            else:
                notificacion(driver, f"No se han encontrado casos de '{filtro}' en las siguientes páginas", "warning", time_out=10000)

        # Verificar si hay más casos en las siguientes páginas
        try:
            siguiente_pagina = driver.find_element(By.XPATH, '//a[@rel="next"]')
            siguiente_pagina.click()
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]//tbody/tr'))
            )
            print("Redireccionando a la siguiente página")
        except:
            print("No hay más páginas")
            break

    # Consolidar datos en una sola lista
    datos_consolidados = []
    for lista in datos.values():
        datos_consolidados.extend(lista)
    
    return datos_consolidados

def notificacion(driver, mensaje, tipo, time_out=10000):
    # Esperar un momento para asegurarse de que Toastr esté cargado
    driver.implicitly_wait(2)

    # Ejecutar el script de Toastr para mostrar la notificación
    toastr_script = f'''
        toastr.options.timeOut = {time_out}; // Tiempo personalizado
        toastr.options.extendedTimeOut = {time_out // 2}; // Tiempo adicional
        toastr.options.positionClass = 'toast-top-right';
        toastr.options.closeButton = true;
        toastr.options.preventDuplicates = true;
        toastr.options.hideDuration = 300;
        toastr.options.showDuration = 300;
        toastr.options.newestOnTop = false;
        toastr["{tipo}"]("{mensaje}");
    '''
    driver.execute_script(toastr_script)
