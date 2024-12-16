import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from urp_from_to import UrbanRoutesPage
from travel_and_transportation import Transportation
from style_of_travel import ComfortOption
from phone_number_button import PhoneNumber
from payment_method import PaymentMethod
from driver_message import DriverMessage
from additional_comfort_category import ComfortTrip


class TestUrbanRoutes:
    driver = None
    urp_from_to = None
    type_transportation = None
    style_of_travel = None
    phone_number_field = None
    payment_method = None
    driver_message = None
    comfort_category = None

    @classmethod
    def setup_class(cls):
        # # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        # from selenium.webdriver import DesiredCapabilities
        # capabilities = DesiredCapabilities.CHROME
        # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.urban_routes_url)
        cls.driver.implicitly_wait(10)

        # Inicializa las páginas
        cls.urp_from_to = UrbanRoutesPage(cls.driver)
        cls.type_transportation = Transportation(cls.driver)
        cls.style_of_travel = ComfortOption(cls.driver)
        cls.phone_number_field = PhoneNumber(cls.driver)
        cls.payment_method = PaymentMethod(cls.driver)
        cls.driver_message = DriverMessage(cls.driver)
        cls.comfort_category = ComfortTrip(cls.driver)

        urp_from_to_data = cls.urp_from_to
        urp_from_to_data.set_from()
        urp_from_to_data.set_to()

        transportation_data = cls.type_transportation
        transportation_data.click_flash_mode()
        transportation_data.click_taxi_mode()
        transportation_data.click_ask_for_taxi()

        style_of_travel_data = cls.style_of_travel
        style_of_travel_data.click_comfort_mode()

    def test_fill_field_from_to(self):
        """Prueba el proceso de llenar los campos de direccion"""
        urp_from_to_data = self.urp_from_to
        urp_from_to_data.set_from()
        urp_from_to_data.set_to()


    def test_request_taxi(self):
        """Solicita un taxi seleccionando el modo de transporte."""
        transportation_data = self.type_transportation
        transportation_data.click_flash_mode()
        transportation_data.click_taxi_mode()
        transportation_data.click_ask_for_taxi()

        style_of_travel_data = self.style_of_travel
        style_of_travel_data.click_comfort_mode()

    def test_fill_phone_number(self):
        """Rellena el número de teléfono y recupera el código de confirmación."""
        phone_number_field_data = self.phone_number_field
        phone_number_field_data.click_phone_button()
        phone_number_field_data.fill_phone_number()
        phone_number_field_data.click_phone_confirmation()
        phone_number_field_data.modal_for_sms_confirmation()
        phone_number_field_data.retrieve_phone_code()

    def test_add_payment_method(self):
        """Agrega un método de pago."""
        payment_method_data = self.payment_method
        payment_method_data.click_payment_method()
        payment_method_data.click_add_card()
        payment_method_data.fill_card_number()
        payment_method_data.fill_card_code()
        payment_method_data.click_add_card_button()
        payment_method_data.verification_close()

    def test_send_driver_message(self):
        """Envía un mensaje al conductor."""
        driver_message_data = self.driver_message
        driver_message_data.driver_message()

    def test_request_additional_comfort(self):
        """Solicita comodidad adicional."""
        comfort_category_data = self.comfort_category
        comfort_category_data.blanket_and_kleenex()
        comfort_category_data.ice_cream()

    # def test_complete_taxi_request_process(self):
    #     """Prueba el proceso completo de solicitud de taxi."""
    #     self.test_fill_field_from_to()
    #     self.test_request_taxi()
    #     self.test_fill_phone_number()
    #     self.test_add_payment_method()
    #     self.test_send_driver_message()
    #     self.test_request_additional_comfort()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
