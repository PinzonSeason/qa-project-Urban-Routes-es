from selenium import webdriver
from selenium.webdriver.common.by import By
import data
import time



class PaymentMethod:

    def __init__(self, driver):
        self.driver = driver

    def click_payment_method(self):
        self.driver.find_element(By.XPATH, BUTTON_PAYMENT).click()

    def click_add_card(self):
        self.driver.find_element(By.XPATH, ADD_CARD).click()

    def fill_card_number(self):
        card_number_input = self.driver.find_element(By.XPATH, INPUT_CARD_NUMBER)
        card_number_input.clear()
        card_number_input.send_keys(data.card_number)

    def fill_card_code(self):
        card_code_input = self.driver.find_element(By.XPATH, INPUT_CARD_CODE)
        card_code_input.clear()
        card_code_input.send_keys(data.card_code)

    def click_add_card_button(self):
        self.driver.find_element(By.XPATH, CONFIRMATION_OF_ADDING).click()

    def verification_close(self):
        time.sleep(2)
        # Verifica si la tarjeta se ha agregado (puedes ajustar el localizador según tu aplicación)
        if self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Tarjeta agregada')]"):
            print("Tarjeta agregada exitosamente.")
            self.driver.find_element(By.XPATH, CLOSE_MODAL_BUTTON).click()
        else:
            print("No se pudo agregar la tarjeta.")

