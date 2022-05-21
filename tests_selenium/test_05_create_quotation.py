from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import time
import testutils

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

class register_login_test(unittest.TestCase):

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_create_quotation_accept(self):
        driver = self.driver
        testutils.login_service_provider(driver)
        assert "testdienstleister1@test.com" in driver.page_source
        testutils.create_quotation_accept(driver)
        assert "Angebotspreis:" in driver.page_source
        assert "300.00 €" in driver.page_source
    
    def test_create_quotation_reject(self):
        driver = self.driver
        testutils.login_service_provider(driver)
        assert "testdienstleister1@test.com" in driver.page_source
        testutils.create_quotation_reject(driver)
        assert "Angebotspreis:" in driver.page_source
        assert "75.00 €" in driver.page_source
            
    def test_create_quotation_confirm(self):
        driver = self.driver
        testutils.login_service_provider(driver)
        assert "testdienstleister1@test.com" in driver.page_source
        testutils.create_quotation_confirm(driver)
        assert "Angebotspreis:" in driver.page_source
        assert "1.00 €" in driver.page_source
        

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(warnings='ignore')