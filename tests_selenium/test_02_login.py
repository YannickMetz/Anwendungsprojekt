from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import testutils

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

class login_test(unittest.TestCase):

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_login_customer(self):
        driver = self.driver
        #testutils.register_customer(driver)
        #ids "actions" und "logout" zu html code hinzugefügt
        #driver.find_element(By.ID, "actions").click()
        #driver.find_element(By.ID, "logout").click()
        testutils.login_customer(driver)
        assert "testkunde1@test.com" in driver.page_source

    def test_login_service_provider(self):
        driver = self.driver
        #testutils.register_service_provider(driver)
        #driver.find_element(By.ID, "actions").click()
        #driver.find_element(By.ID, "logout").click()
        testutils.login_service_provider(driver)
        assert "testdienstleister1@test.com" in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(warnings='ignore')