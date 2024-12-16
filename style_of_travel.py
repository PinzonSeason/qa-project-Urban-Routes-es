from selenium import webdriver
from selenium.webdriver.common.by import By
import data

#Selectors
ICON_COMFORT_RATE = "//img[@src='/static/media/kids.075fd8d4.svg']"

class ComfortOption:

    def __init__(self, driver):
        self.driver = driver

    def click_comfort_mode(self):
        self.driver.find_element(By.XPATH, ICON_COMFORT_RATE).click()

