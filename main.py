from selenium import webdriver
from inicio_sesion import iniciar_sesion
from navegar import navegar_al_proyecto
from extraer_datos import extraer_datos, notificacion, agregar_toastr
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

            # Navegacion de componentes
            navegar_al_proyecto(driver)

            # Agregar Toastr para notificaciones
            agregar_toastr(driver)

            # Filtrar casos para los nombres especificados
            filtros = [
                "BAC InfraNoProd", "Giovanni Castelblanco", "Steven Garcia",
                "Raul Garzon", "Fabian Pinto", "Andres Sandoval",
                "Cristian Gonzalez", "Sandra Gutierrez", "Andres Muñoz"
            ]

            # Extraer datos y consolidar
            datos_consolidados = extraer_datos(driver, filtros)

            if datos_consolidados:
                df_consolidados = pd.DataFrame(datos_consolidados)
                with pd.ExcelWriter('reporte.xlsx', engine='openpyxl') as writer:
                    df_consolidados.to_excel(writer, sheet_name='Consolidado', index=False)
                    formatear_columnas(writer.sheets['Consolidado'])

                notificacion(driver, "Casos extraídos y guardados en reporte.xlsx", "success", time_out=60000)
            else:
                notificacion(driver, "No se ha extraído información", "warning", time_out=60000)

            # Esperar para asegurar que la notificación sea visible
            time.sleep(45)

            driver.quit()


def formatear_columnas(worksheet):
    
            # Ajustar el formato de las columnas
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

if __name__ == "__main__":
    main()
