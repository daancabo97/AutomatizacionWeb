from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def iniciar_sesion(driver, url, usuario, contrasena):
        
        driver.get(url)
        
        # Esperar a que la página cargue
        time.sleep(2)
        
        # Ingresar credenciales
        campo_usuario = driver.find_element(By.NAME, 'username')
        campo_contrasena = driver.find_element(By.NAME, 'password')
        
        campo_usuario.send_keys(usuario)
        campo_contrasena.send_keys(contrasena)
        campo_contrasena.send_keys(Keys.RETURN)
        
        # Esperar a que redireccione a la siguiente pagina
        time.sleep(3)
