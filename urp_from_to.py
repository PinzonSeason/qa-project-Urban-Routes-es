from selenium import webdriver
from selenium.webdriver.common.by import By
import data
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# Localizadores
INPUT_FROM_FIELD_XPATH = '//input[@id="from"]'
#INPUT_FROM_FIELD_XPATH = '//input[@class="label" and @for="from"]'
INPUT_TO_FIELD_XPATH = '//input[@id="to"]'

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self):
        self.driver.find_element(By.XPATH, INPUT_FROM_FIELD_XPATH).send_keys(data.address_from)

    def set_to(self):
        self.driver.find_element(By.XPATH, INPUT_TO_FIELD_XPATH).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

