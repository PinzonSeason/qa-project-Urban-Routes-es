from selenium import webdriver
from selenium.webdriver.common.by import By
import data

#Selectors
INPUT_DRIVER_MESSAGE = "//label[text()='Mensaje para el conductor...']"

class DriverMessage:

    def __init__(self, driver):
        self.driver = driver

    def driver_message(self):
        self.driver.find_element(By.XPATH, INPUT_DRIVER_MESSAGE).send_keys(data.message_for_driver)