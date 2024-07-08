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

    # Proceso de inicio de sesión
    iniciar_sesion(driver, url, usuario, contrasena)

    # Navegar al proyecto específico
    navegar_al_proyecto(driver)

    # Extraer datos y exportar a Excel
    datos = extraer_datos(driver)
    df = pd.DataFrame(datos)
    df.to_excel('output.xlsx', index=False)

    driver.quit()

if __name__ == "__main__":
    main()
