from time import sleep
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urban_routes_page import UrbanRoutesPage

class TestUrbanRoutes:
    driver = None
    urp_from_to = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        # from selenium.webdriver import DesiredCapabilities
        # capabilities = DesiredCapabilities.CHROME
        # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

        # Configurar el navegador para habilitar los logs de rendimiento
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")

        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(5)

    def setup_method(self):
        self.driver.get(data.urban_routes_url)
        self.urp_from_to = UrbanRoutesPage(self.driver)
        self.urp_from_to.set_from()
        self.urp_from_to.set_to()

    def test_set_route(self):
        """Try the process of filling the address fields"""
        urp_from_to_data = self.urp_from_to

        assert urp_from_to_data.get_from(), "El campo 'Desde' no se llenó correctamente."
        assert urp_from_to_data.get_to(), "El campo 'Hasta' no se llenó correctamente."

    def test_select_plan(self):
        """Request a taxi by selecting the transport mode."""
        select_plan_data = self.urp_from_to

        select_plan_data.click_flash_mode()
        select_plan_data.click_taxi_mode()
        select_plan_data.click_ask_for_taxi()

    def test_fill_phone_number(self):
        """Fill in the phone number and recover the confirmation code."""
        phone_number_field_data = self.urp_from_to

        phone_number_field_data.click_flash_mode()
        phone_number_field_data.click_taxi_mode()
        phone_number_field_data.click_ask_for_taxi()
        phone_number_field_data.click_comfort_mode()

        phone_number_field_data.click_phone_button()
        phone_number_field_data.fill_phone_number()
        phone_number_field_data.click_phone_confirmation()
        phone_number_field_data.click_close_button_section_close()

    def test_fill_card(self):
        """Add a payment method."""
        payment_method_data = self.urp_from_to
        payment_method_data.click_flash_mode()
        payment_method_data.click_taxi_mode()
        payment_method_data.click_ask_for_taxi()
        payment_method_data.click_comfort_mode()

        payment_method_data.click_payment_method()
        payment_method_data.click_add_card()
        payment_method_data.fill_card_number()
        payment_method_data.fill_card_code()
        payment_method_data.click_edge_modal_add_card()
        payment_method_data.click_add_card_button()
        payment_method_data.verification_close()

    def test_comment_for_driver(self):
        """Send a message to the driver."""
        driver_message_data = self.urp_from_to

        driver_message_data.click_flash_mode()
        driver_message_data.click_taxi_mode()
        driver_message_data.click_ask_for_taxi()
        driver_message_data.click_comfort_mode()

        driver_message_data.driver_message()

    def test_order_blanket_and_handkerchiefs(self):
        """Request additional comfort."""
        comfort_category_data = self.urp_from_to

        comfort_category_data.click_flash_mode()
        comfort_category_data.click_taxi_mode()
        comfort_category_data.click_ask_for_taxi()
        comfort_category_data.click_comfort_mode()

        comfort_category_data.blanket_and_kleenex()


    def test_order_2_ice_creams(self):
        """Try the full taxi application process."""
        ice_cream_data = self.urp_from_to

        ice_cream_data.click_flash_mode()
        ice_cream_data.click_taxi_mode()
        ice_cream_data.click_ask_for_taxi()
        ice_cream_data.click_comfort_mode()

        ice_cream_data.ice_cream()
        ice_cream_data.ice_cream()


    def test_car_search_model_appears(self):
        """Wait until the emerging window appears (car search)."""
        #Para esto necesito interactuar con retrieve_phone_code, el cual no he podido decifrar, lo modifique a un selenium mas actual y aun asi no pude, no entiendo el tema de los logs
        pass

    def test_driver_info_appears(self):
        """Wait until the driver's information appears."""
        pass

    @classmethod
    def teardown_class(cls):
        sleep(5)  #Wait 5 seconds to observe the result before closing
        cls.driver.quit()
