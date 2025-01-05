import time
from time import (sleep)
import data
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # Selector for routes
    INPUT_FROM_FIELD_ID = (By.XPATH, "//input[@id='from']")
    INPUT_TO_FIELD_XPATH = (By.XPATH, "//input[@id='to']")

    # Selector for travel
    ICON_FLASH = (By.XPATH, "//div[contains(@class, 'mode') and contains(@class, 'active')]")
    ICON_TAXI = (By.XPATH, "//img[@src='/static/media/taxi-active.b0be3054.svg']")
    BUTTON_ASK_FOR_TAXI = (By.XPATH, "//button[text()='Pedir un taxi']")

    # Selector for rate
    ICON_COMFORT_RATE = (By.XPATH, "//img[@src='/static/media/kids.075fd8d4.svg']")

    # Selector for phone number
    BUTTON_PHONE_NUMBER = (By.CSS_SELECTOR, ".np-text")
    FIELD_PHONE_NUMBER_ID = (By.CSS_SELECTOR, '#phone')
    BUTTON_PN_CONFIRMATION = (By.XPATH, "//button[text()='Siguiente']")
    FIELD_CODE = (By.XPATH, "//label[text()='Introduce el código']")
    BUTTON_SMS_CONFIRMATION = (By.XPATH, "//button[text()='Confirmar']")
    BUTTON_TO_CLOSE_SMS_CON = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[2]/button")

    # Selector for payment method
    BUTTON_PAYMENT = (By.CLASS_NAME, "pp-text")
    ADD_CARD = (By.XPATH, "//div[@class='pp-title' and text()='Agregar tarjeta']")
    INPUT_CARD_NUMBER = (By.ID, "number")
    INPUT_CARD_CODE = (By.CSS_SELECTOR, "input[name='code']")
    CLICK_ON_EDGE_MODAL = (By.XPATH, "//div[@class='section active unusual']")
    CONFIRMATION_OF_ADDING = (By.XPATH, "//form[div[3]/button]/div[3]/button[1]")
    CLOSE_MODAL_BUTTON = (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")

    # Selector for a driver
    CLICK_INPUT_DRIVER_MESSAGE = (By.XPATH, "//*[@id='root']/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/label")
    FILL_DRIVER_MESSAGE = (By.XPATH, "//*[@id='comment']")

    # Selector for additional information
    SLIDER_ROUND_BLANKET_AND_KLEENEX = (By.CSS_SELECTOR, ".slider.round")
    COUNTER_PLUS_ICE_CREAM = (By.CSS_SELECTOR, ".counter-plus")

    def __init__(self, driver):
        self.driver = driver

#---------------------------------------------------------------------------------------------------------
    """SET ROUTE"""

    def set_from(self):
        self.driver.find_element(*self.INPUT_FROM_FIELD_ID).send_keys(data.address_from)

    def set_to(self):
        self.driver.find_element(*self.INPUT_TO_FIELD_XPATH).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

#--------------------------------------------------------------------------------------------------------
    """TYPE OF TRAVEL"""

    def click_flash_mode(self):
        self.driver.find_element(*self.ICON_FLASH).click()


    def click_taxi_mode(self):
        self.driver.find_element(*self.ICON_TAXI).click()

    def click_ask_for_taxi(self):
        self.driver.find_element(*self.BUTTON_ASK_FOR_TAXI).click()


    def click_comfort_mode(self):
        self.driver.find_element(*self.ICON_COMFORT_RATE).click()

#--------------------------------------------------------------------------------------------------------
    """PHONE NUMBER"""

    def click_phone_button(self):
        self.driver.find_element(*self.BUTTON_PHONE_NUMBER).click()

    def fill_phone_number(self):
        self.driver.find_element(*self.FIELD_PHONE_NUMBER_ID).send_keys(data.phone_number)

    def click_phone_confirmation(self):
        self.driver.find_element(*self.BUTTON_PN_CONFIRMATION).click()

    def retrieve_phone_code(self) -> str:
        """Recupera el código de confirmación del teléfono desde los logs de rendimiento."""
        code = None
        wait_time = 15  # Aumenta el tiempo de espera
        start_time = time.time()

        while time.time() - start_time < wait_time:
            try:
                # Espera a que se generen los logs de rendimiento
                WebDriverWait(self.driver, 1).until(lambda d: d.get_log('performance'))
                logs = [log["message"] for log in self.driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]

                print("Logs de rendimiento:", logs)  # Imprime los logs para depurar

                for log in reversed(logs):
                    print("Log encontrado:", log)  # Imprime cada log encontrado
                    message_data = json.loads(log)["message"]
                    body = self.driver.execute_cdp_cmd('Network.getResponseBody',
                                                       {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
                    if code:  # Si se encontró el código, salir del bucle
                        return code
            except (WebDriverException, TimeoutException) as e:
                print(f"Error al recuperar el código: {e}")  # Imprime el error para depurar
                continue  # Ignorar excepciones y seguir intentando

        raise Exception("No se encontró el código de confirmación del teléfono.\n"
                        "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")

    def modal_for_sms_confirmation(self):
        code = self.retrieve_phone_code()
        self.driver.find_element(*self.FIELD_CODE).send_keys(code)
        self.driver.find_element(*self.BUTTON_SMS_CONFIRMATION).click()

    def click_close_button_section_close(self):
        self.driver.find_element(*self.BUTTON_TO_CLOSE_SMS_CON).click()

#--------------------------------------------------------------------------------------------------------
    """PAYMENT METHOD"""

    def click_payment_method(self):
        self.driver.find_element(*self.BUTTON_PAYMENT).click()

    def click_add_card(self):
        self.driver.find_element(*self.ADD_CARD).click()

    def fill_card_number(self):
        try:
            card_number_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.INPUT_CARD_NUMBER)  # Asegúrate de pasar solo la tupla
            )
            card_number_input.clear()
            card_number_input.send_keys(data.card_number)
        except TimeoutException:
            print("El campo de número de tarjeta no se encontró o no es visible.")
        except Exception as e:
            print(f"Ocurrió un error al intentar llenar el número de tarjeta: {e}")

    def fill_card_code(self):
        try:
            card_code_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.INPUT_CARD_CODE)  # Asegúrate de pasar solo la tupla
            )
            card_code_input.clear()
            card_code_input.send_keys(data.card_code)
        except TimeoutException:
            print("El campo de código de tarjeta no se encontró o no es visible.")
        except Exception as e:
            print(f"Ocurrió un error al intentar llenar el código de tarjeta: {e}")

    def click_edge_modal_add_card(self):
        self.driver.find_element(*self.CLICK_ON_EDGE_MODAL).click()

    def click_add_card_button(self):
        # card_number_input = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.ID, INPUT_CARD_NUMBER))
        # )
        self.driver.find_element(*self.CONFIRMATION_OF_ADDING).click()

    def verification_close(self):
        time.sleep(5)
        if self.driver.find_elements(By.XPATH, "//div[@class='pp-title' and text()='Tarjeta']"):
            print("Tarjeta agregada exitosamente.")
            # Esperar hasta que el botón de cerrar sea clickeable
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CLOSE_MODAL_BUTTON)
            )
            close_button.click()
        else:
            print("No se pudo agregar la tarjeta.")

#--------------------------------------------------------------------------------------------------------
    """ADDITIONAL INFORMATION"""

    def driver_message(self):
        self.driver.find_element(*self.CLICK_INPUT_DRIVER_MESSAGE).click()
        self.driver.find_element(*self.FILL_DRIVER_MESSAGE).send_keys(data.message_for_driver)
    def blanket_and_kleenex(self):
        self.driver.find_element(*self.SLIDER_ROUND_BLANKET_AND_KLEENEX).click()

    def ice_cream(self):
        self.driver.find_element(*self.COUNTER_PLUS_ICE_CREAM).click()