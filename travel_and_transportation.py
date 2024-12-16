from selenium import webdriver
from selenium.webdriver.common.by import By
import data

# Selectors
ICON_FLASH = "//div[contains(@class, 'mode') and contains(@class, 'active')]"
ICON_TAXI = "//img[@src='/static/media/taxi-active.b0be3054.svg']"
BUTTON_ASK_FOR_TAXI = "//button[text()='Pedir un taxi']"

class Transportation:

    def __init__(self, driver):
        self.driver = driver

    def click_flash_mode(self):
        self.driver.find_element(By.XPATH, ICON_FLASH).click()

    def click_taxi_mode(self):
        self.driver.find_element(By.XPATH, ICON_TAXI).click()

    def click_ask_for_taxi(self):
        self.driver.find_element(By.XPATH, BUTTON_ASK_FOR_TAXI).click()




# Inicializa el controlador
driver = webdriver.Chrome()
driver.get(data.urban_routes_url)  # Cambia a la URL de tu elección

try:
    # Intenta encontrar el elemento usando tu localizador
    element = driver.find_element(By.XPATH, "//div[contains(@class, 'mode') and contains(@class, 'active')]")
    print("Localizador correcto, elemento encontrado:", element)
except Exception as e:
    print("Error al encontrar el elemento:", e)

# Cierra el navegador
driver.quit()