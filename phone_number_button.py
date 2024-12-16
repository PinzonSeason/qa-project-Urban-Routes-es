from selenium import webdriver
from selenium.webdriver.common.by import By
import data

#Selectors
BUTTON_PHONE_NUMBER = "//div[text()='Número de teléfono']"
FIELD_PHONE_NUMBER = "//label[text()='Número de teléfono']"
BUTTON_PN_CONFIRMATION = "//button[text()='Siguiente']"
FIELD_CODE = "//label[text()='Introduce el código']"
BUTTON_SMS_CONFIRMATION = "//button[text()='Confirmar']"

class PhoneNumber:

    def __init__(self, driver):
        self.driver = driver

    def click_phone_button(self):
        self.driver.find_element(By.XPATH, BUTTON_PHONE_NUMBER).click()

    def fill_phone_number(self):
        self.driver.find_element(By.XPATH, FIELD_PHONE_NUMBER).send_keys(data.phone_number)

    def click_phone_confirmation(self):
        self.driver.find_element(By.XPATH, BUTTON_PN_CONFIRMATION).click()

    def modal_for_sms_confirmation(self):
        code = self.retrieve_phone_code(self.driver)
        self.driver.find_element(By.XPATH, FIELD_CODE).send_keys(code)
        self.driver.find_element(By.XPATH, BUTTON_SMS_CONFIRMATION).click()

    # no modificar
    def retrieve_phone_code(driver) -> str:
        """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
        Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
        El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

        import json
        import time
        from selenium.common import WebDriverException
        code = None
        for i in range(10):
            try:
                logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = driver.execute_cdp_cmd('Network.getResponseBody',
                                                  {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
            except WebDriverException:
                time.sleep(1)
                continue
            if not code:
                raise Exception("No se encontró el código de confirmación del teléfono.\n"
                                "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
            return codegit