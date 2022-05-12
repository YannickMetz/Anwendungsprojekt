from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import testutils
import time

#deprecated befehle für hausarbeit beachten. umsetzung und quellen 
#find_element_by.... ist jetzt find_element(By....)
#chromedriver.exe nicht mehr notwendig. ChromeDriverManager läd automatisch den Chromedriver herunter.

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

class register_test(unittest.TestCase, unittest.TextTestResult):
    @classmethod
    def setUpClass(cls):
        testutils.reset_db()

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_register_customer(self):
        driver = self.driver
        testutils.register_customer(driver)
        #überprüfen ob alle felder mit "required" ausgefüllt sind
        assert "This field is required." not in driver.page_source
        #prüfen ob registrierter user automatisch eingeloggt wurde
        assert "testkunde1@test.com" in driver.page_source

    def test_register_service_provider(self):
        driver = self.driver
        testutils.register_service_provider(driver)
        #überprüfen ob alle felder mit "required" ausgefüllt sind
        assert "This field is required." not in driver.page_source
        #prüfen ob registrierter user automatisch eingeloggt wurde
        assert "testdienstleister1@test.com" in driver.page_source 

    def tearDown(self):
        self.driver.close()
    
        
if __name__ == "__main__":
    #warnings=ignore um unclosed socket warnung zu unterbinden
    unittest.main(warnings='ignore')