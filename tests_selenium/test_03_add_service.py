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

class add_service_test(unittest.TestCase):

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_add_service(self):
        driver = self.driver
        testutils.login_service_provider(driver)
        assert "testdienstleister1@test.com" in driver.page_source
        testutils.add_service(driver)
        self.assertTrue(driver.find_element(By.ID, "Garten"))
        self.assertTrue(driver.find_element(By.ID, "Fassade"))
        self.assertTrue(driver.find_element(By.ID, "Möbelaufbau"))

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(warnings='ignore')