import pickle
from selenium import webdriver

# Crear una instancia del WebDriver de Chrome
driver = webdriver.Chrome()

# Navegar a una página web (asegúrate de haber iniciado sesión previamente)
driver.get("https://www.google.com")

# Obtener las cookies del navegador
if input("Igresa para con") == "X":
    cookies = driver.get_cookies()

    # Guardar las cookies en un archivo
    with open("cookies.pkl", "wb") as file:
        pickle.dump(cookies, file)

    # Cerrar el navegador
    driver.quit()
