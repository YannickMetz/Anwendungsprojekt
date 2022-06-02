from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import testutils

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

class request_quotation_test(unittest.TestCase):

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_request_quotation_accept(self):
        driver = self.driver
        testutils.login_customer(driver)
        assert "testkunde1@test.com" in driver.page_source
        testutils.request_quotation_accept(driver)
        assert "Angebotsanfrage erfolgreich übermittelt." in driver.page_source

    def test_request_quotation_reject(self):
        driver = self.driver
        testutils.login_customer(driver)
        assert "testkunde1@test.com" in driver.page_source
        testutils.request_quotation_reject(driver)
        assert "Angebotsanfrage erfolgreich übermittelt." in driver.page_source
    
    def test_request_quotation_confirm(self):
        driver = self.driver
        testutils.login_customer(driver)
        assert "testkunde1@test.com" in driver.page_source
        testutils.request_quotation_confirm(driver)
        assert "Angebotsanfrage erfolgreich übermittelt." in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(warnings='ignore')