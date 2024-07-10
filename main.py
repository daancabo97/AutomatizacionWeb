from selenium import webdriver
from inicio_sesion import iniciar_sesion
from navegar import navegar_al_proyecto
from extraer_datos import extraer_datos
import pandas as pd

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

        # Extraer datos y exportar a Excel
        datos = extraer_datos(driver)
        if datos:
            df = pd.DataFrame(datos)
            formatear_columnas(df, 'reporte.xlsx')
            print("Casos extraídos y guardados")
        else:
            print("No se ha extraído información")

        driver.quit()


def formatear_columnas(df, filepath):

        writer = pd.ExcelWriter(filepath, engine='openpyxl')
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']


        # Ajustar el ancho de las columnas
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter  # Obtener el nombre de la columna
            for celda in col:
                try:
                    if len(str(celda.value)) > max_length:
                        max_length = len(celda.value)
                except:
                    pass
            ajustar_anchura = (max_length + 2)
            worksheet.column_dimensions[column].width = ajustar_anchura

        writer.close()

if __name__ == "__main__":
    main()
