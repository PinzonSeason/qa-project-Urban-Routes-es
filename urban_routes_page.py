from selenium import webdriver
from selenium.webdriver.common.by import By
import data
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait



#Selector for routes
INPUT_FROM_FIELD_ID = "//input[@id='from']"
#INPUT_FROM_FIELD_XPATH = '//input[@class="label" and @for="from"]'
INPUT_TO_FIELD_XPATH = "//input[@id='to']"

#Selector for travel
ICON_FLASH = "//div[contains(@class, 'mode') and contains(@class, 'active')]"
ICON_TAXI = "//img[@src='/static/media/taxi-active.b0be3054.svg']"
BUTTON_ASK_FOR_TAXI = "//button[text()='Pedir un taxi']"

#Selector for rate
ICON_COMFORT_RATE = "//img[@src='/static/media/kids.075fd8d4.svg']"

#Selector for phone number
BUTTON_PHONE_NUMBER = ".np-text"
FIELD_PHONE_NUMBER_ID = '#phone'
BUTTON_PN_CONFIRMATION = "//button[text()='Siguiente']"
FIELD_CODE = "//label[text()='Introduce el código']"
BUTTON_SMS_CONFIRMATION = "//button[text()='Confirmar']"
BUTTON_TO_CLOSE_SMS_CON = "/html/body/div/div/div[1]/div[2]/div[2]/button"

#Selector for payment method
BUTTON_PAYMENT = "pp-text"
ADD_CARD = "//div[@class='pp-title' and text()='Agregar tarjeta']"
INPUT_CARD_NUMBER = "number"
INPUT_CARD_CODE = "input[name='code']"
CLICK_ON_EDGE_MODAL = "//div[@class='section active unusual']"
CONFIRMATION_OF_ADDING = "//form[div[3]/button]/div[3]/button[1]"
CLOSE_MODAL_BUTTON = "//*[@id='root']/div/div[2]/div[2]/div[1]/button"

#Selector for a driver
INPUT_DRIVER_MESSAGE = "comment"

#Selector for additional information
SLIDER_ROUND_BLANKET_AND_KLEENEX = ".slider.round"
COUNTER_PLUS_ICE_CREAM = ".counter-plus"


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

#---------------------------------------------------------------------------------------------------------
    """SET ROUTE"""

    def set_from(self):
        self.driver.find_element(By.XPATH, INPUT_FROM_FIELD_ID).send_keys(data.address_from)

    def set_to(self):
        self.driver.find_element(By.XPATH, INPUT_TO_FIELD_XPATH).send_keys(data.address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

#--------------------------------------------------------------------------------------------------------
    """TYPE OF TRAVEL"""

    def click_flash_mode(self):
        self.driver.find_element(By.XPATH, ICON_FLASH).click()


    def click_taxi_mode(self):
        self.driver.find_element(By.XPATH, ICON_TAXI).click()

    def click_ask_for_taxi(self):
        self.driver.find_element(By.XPATH, BUTTON_ASK_FOR_TAXI).click()


    def click_comfort_mode(self):
        self.driver.find_element(By.XPATH, ICON_COMFORT_RATE).click()

#--------------------------------------------------------------------------------------------------------
    """PHONE NUMBER"""

    def click_phone_button(self):
        self.driver.find_element(By.CSS_SELECTOR, BUTTON_PHONE_NUMBER).click()

    def fill_phone_number(self):
        self.driver.find_element(By.CSS_SELECTOR, FIELD_PHONE_NUMBER_ID).send_keys(data.phone_number)

    def click_phone_confirmation(self):
        self.driver.find_element(By.XPATH, BUTTON_PN_CONFIRMATION).click()

    # # no modificar
    # def retrieve_phone_code(driver) -> str:
    #     """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    #     Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    #     El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
    #
    #     import json
    #     import time
    #     from selenium.common import WebDriverException
    #     code = None
    #     for i in range(10):
    #         try:
    #             logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
    #                     and 'api/v1/number?number' in log.get("message")]
    #             for log in reversed(logs):
    #                 message_data = json.loads(log)["message"]
    #                 body = driver.execute_cdp_cmd('Network.getResponseBody',
    #                                               {'requestId': message_data["params"]["requestId"]})
    #                 code = ''.join([x for x in body['body'] if x.isdigit()])
    #         except WebDriverException:
    #             time.sleep(1)
    #             continue
    #         if not code:
    #             raise Exception("No se encontró el código de confirmación del teléfono.\n"
    #                             "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
    #         return code
    def retrieve_phone_code(driver) -> str:
        """Devuelve un número de confirmación de teléfono como un string.
        Asegúrate de haber solicitado el código en la aplicación antes de usar esta función."""

        import json
        import time
        from selenium.common import WebDriverException

        for _ in range(10):  # Intenta 10 veces
            try:
                # Obtiene los logs de rendimiento
                logs = driver.get_log('performance')
                # Filtra los logs que contienen el mensaje de la API
                for log in logs:
                    if 'api/v1/number?number' in log.get("message", ""):
                        message_data = json.loads(log["message"])
                        request_id = message_data["params"]["requestId"]
                        # Obtiene el cuerpo de la respuesta
                        body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                        # Extrae los dígitos del cuerpo
                        code = ''.join(filter(str.isdigit, body['body']))
                        if code:  # Si se encontró el código
                            return code
            except WebDriverException:
                time.sleep(1)  # Espera un segundo antes de volver a intentar

        raise Exception("No se encontró el código de confirmación del teléfono. "
                        "Asegúrate de haber solicitado el código en tu aplicación.")

    def modal_for_sms_confirmation(self):
        code = self.retrieve_phone_code(self)
        self.driver.find_element(By.XPATH, FIELD_CODE).send_keys(code)
        self.driver.find_element(By.XPATH, BUTTON_SMS_CONFIRMATION).click()

    def click_close_button_section_close(self):
        self.driver.find_element(By.XPATH, BUTTON_TO_CLOSE_SMS_CON).click()

#--------------------------------------------------------------------------------------------------------
    """PAYMENT METHOD"""

    def click_payment_method(self):
        self.driver.find_element(By.CLASS_NAME, BUTTON_PAYMENT).click()

    def click_add_card(self):
        self.driver.find_element(By.XPATH, ADD_CARD).click()

    def fill_card_number(self):
        card_number_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, INPUT_CARD_NUMBER))
        )
        card_number_input.clear()
        card_number_input.send_keys(data.card_number)

    def fill_card_code(self):
        card_code_input = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, INPUT_CARD_CODE))
        )
        card_code_input.clear()
        card_code_input.send_keys(data.card_code)

    def click_edge_modal_add_card(self):
        self.driver.find_element(By.XPATH, CLICK_ON_EDGE_MODAL).click()

    def click_add_card_button(self):
        # card_number_input = WebDriverWait(self.driver, 10).until(
        #     EC.visibility_of_element_located((By.ID, INPUT_CARD_NUMBER))
        # )
        self.driver.find_element(By.XPATH, CONFIRMATION_OF_ADDING).click()

    def verification_close(self):
        time.sleep(5)
        if self.driver.find_elements(By.XPATH, "//div[@class='pp-title' and text()='Tarjeta']"):
            print("Tarjeta agregada exitosamente.")
            # Esperar hasta que el botón de cerrar sea clickeable
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, CLOSE_MODAL_BUTTON))
            )
            close_button.click()
        else:
            print("No se pudo agregar la tarjeta.")

#--------------------------------------------------------------------------------------------------------
    """ADDITIONAL INFORMATION"""

    def driver_message(self):
        self.driver.find_element(By.ID, INPUT_DRIVER_MESSAGE).send_keys(data.message_for_driver)

    def blanket_and_kleenex(self):
        self.driver.find_element(By.CSS_SELECTOR, SLIDER_ROUND_BLANKET_AND_KLEENEX).click()

    def ice_cream(self):
        self.driver.find_element(By.CSS_SELECTOR, COUNTER_PLUS_ICE_CREAM).click()