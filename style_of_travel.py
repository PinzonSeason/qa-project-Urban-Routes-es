from selenium import webdriver
from selenium.webdriver.common.by import By
import data



class ComfortOption:

    def __init__(self, driver):
        self.driver = driver

    def click_comfort_mode(self):
        self.driver.find_element(By.XPATH, ICON_COMFORT_RATE).click()

