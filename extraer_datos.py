from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def extraer_datos(driver, filtros):

            datos = {filtro: [] for filtro in filtros}
            pagina_actual = 1

            while True:
                # URL de la página actual
                url = f'https://servicedesk.cobiscorp.com/projects/bac-soporte-infraestructura/issues?page={pagina_actual}'
                driver.get(url)

                # Esperar a que la tabla cargue
                try:
                    table = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//table[contains(@class, "list issues")]'))
                    )
                    print(f"Evidencias encontradas en la página {pagina_actual}")
                except TimeoutException as e:
                    print(f"Error al encontrar incidencias en la tabla: {e}")
                    break

                filas = table.find_elements(By.XPATH, './/tbody/tr')
                casos_capturados_pagina = {filtro: 0 for filtro in filtros}
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
                                casos_capturados_pagina[filtro] += 1
                                break

                # Notificación de casos capturados para cada filtro
                for filtro in filtros:
                    if casos_capturados_pagina[filtro] > 0:
                        notificacion(driver, f"Se han capturado: {casos_capturados_pagina[filtro]} casos asignados a {filtro} en la página {pagina_actual}", "info", time_out=10000)
                    else:
                        notificacion(driver, f"No se han encontrado casos de '{filtro}' en la página {pagina_actual}", "warning", time_out=10000)

                # Verificar si hay más casos en las siguientes páginas
                try:
                    siguiente_pagina = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Siguiente »")]'))
                    )
                    siguiente_pagina.click()
                    pagina_actual += 1
                    print(f"Redireccionando a la página {pagina_actual}")
                except (NoSuchElementException, TimeoutException) as e:
                    notificacion(driver, f"No hay más páginas", "info", time_out=10000)
                    break

            # Consolidar datos en una sola lista
            datos_consolidados = []
            for lista in datos.values():
                datos_consolidados.extend(lista)
            
            return datos_consolidados

def notificacion(driver, mensaje, tipo, time_out=10000):
            
            # (Tamaño y posicion de notificacion).
            # Esperar un momento para asegurarse de que Toastr esté cargado
            driver.implicitly_wait(2)

            # Verificar si Toastr está definido
            if not driver.execute_script("return typeof toastr !== 'undefined';"):
                agregar_toastr(driver)

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

def agregar_toastr(driver):
            
            # (Estilos de Notificacion.)
            # Inyectar los scripts y estilos de Toastr
            toastr_css = "https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css"
            toastr_js = "https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"

            driver.execute_script(f'''
                var link = document.createElement("link");
                link.rel = "stylesheet";
                link.type = "text/css";
                link.href = "{toastr_css}";
                document.head.appendChild(link);

                var script = document.createElement("script");
                script.type = "text/javascript";
                script.src = "{toastr_js}";
                document.head.appendChild(script);
            ''')

            # Esperar a que los scripts se carguen
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return typeof toastr !== 'undefined';")
            )
