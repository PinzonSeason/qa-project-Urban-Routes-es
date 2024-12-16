from selenium import webdriver
from selenium.webdriver.common.by import By
import data

#Selectors
SLIDER_ROUND_BLANKET_AND_KLEENEX = "//span[contains(@class, 'slider') and contains(@class, 'round')]"
COUNTER_PLUS_ICE_CREAM = "//div[@class='r-counter-label' and contains(text(), 'Helado')]"

class ComfortTrip:

    def __init__(self, driver):
        self.driver = driver

    def blanket_and_kleenex(self):
        self.driver.find_element(By.XPATH, SLIDER_ROUND_BLANKET_AND_KLEENEX).send_keys(data.message_for_driver)

    def ice_cream(self):
        self.driver.find_element(By.XPATH, COUNTER_PLUS_ICE_CREAM).click()