from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unittest
import os
import string
import random
import testutils
import time

chromedriverpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "chromedriver.exe")

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

#def reset_db():
#    os.system("flask mockdata reset-db")

#random string generator um tests mehrfach ausführen zu können ohne emailadresse und firmenname anpassen zu müssen
def string_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class register_test(unittest.TestCase):
#    @classmethod
#    def setUpClass(cls):
#        reset_db()

    def setUp(self):
        #überprüfen ob chromedriver im pfad vorhanden ansonsten keine tests
        assert os.path.isfile(chromedriverpath) == True
        self.string_output = string_generator()
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(chromedriverpath)
        
    def tearDown(self):
        self.driver.close()

    def test_register_customer(self):
        driver = self.driver
        testutils.register_customer(driver)
        #überprüfen ob alle felder mit "required" ausgefüllt sind
        assert "This field is required." not in driver.page_source
        #prüfen ob registrierter user automatisch eingeloggt wurde
        assert "testkunde1@test.com" in driver.page_source
        time.sleep(5)

    def test_register_service_provider(self):
        driver = self.driver
        testutils.register_service_provider(driver)
        assert "This field is required." not in driver.page_source
        #prüfen ob registrierter user automatisch eingeloggt wurde
        assert "testdienstleister", self.string_output+"@test.com" in driver.page_source

if __name__ == "__main__":
    unittest.main()