# main.py

from selenium import webdriver
from inicio_sesion import iniciar_sesion
from navegar import navegar_al_proyecto
from extraer_datos import extraer_datos
import pandas as pd
import time

def main():
    # Configuración del navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options)

    # URL de la página de inicio de sesión
    url = 'https://servicedesk.cobiscorp.com/login'
    usuario = 'dcaicedo'
    contrasena = 'EC-dansa12*'

    # Parametros de inicio de sesión
    iniciar_sesion(driver, url, usuario, contrasena)

    # Navegar al proyecto específico
    navegar_al_proyecto(driver)

    # Agregar Toastr para notificaciones
    agregar_toastr(driver)

    # Extraer datos y exportar a Excel
    datos_bac_infra = extraer_datos(driver, ["BAC InfraNoProd"])
    datos_giovanni = extraer_datos(driver, ["Giovanni Castelblanco"])
    datos_steven = extraer_datos(driver, ["Steven Garcia"])
    

    if datos_bac_infra or datos_giovanni or datos_steven:
        with pd.ExcelWriter('reporte.xlsx', engine='openpyxl') as writer:
            if datos_bac_infra:
                df_bac_infra = pd.DataFrame(datos_bac_infra)
                df_bac_infra.to_excel(writer, sheet_name='BAC InfraNoProd', index=False)
                formatear_columnas(writer.sheets['BAC InfraNoProd'])
            if datos_giovanni:
                df_giovanni = pd.DataFrame(datos_giovanni)
                df_giovanni.to_excel(writer, sheet_name='Giovanni', index=False)
                formatear_columnas(writer.sheets['Giovanni'])
            if datos_steven:
                df_steven = pd.DataFrame(datos_steven)
                df_steven.to_excel(writer, sheet_name='Steven', index=False)
                formatear_columnas(writer.sheets['Steven'])

        notificacion(driver, "Casos extraídos y guardados en reporte.xlsx", "success", time_out=60000)
    else:
        notificacion(driver, "No se ha extraído información", "warning", time_out=60000)


    # Esperar para asegurar que la notificación sea visible
    time.sleep(30)

    driver.quit()

def formatear_columnas(worksheet):
    # Ajustar el ancho de las columnas
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjust_width = (max_length + 2)
        worksheet.column_dimensions[column].width = adjust_width

def agregar_toastr(driver):
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

if __name__ == "__main__":
    main()
