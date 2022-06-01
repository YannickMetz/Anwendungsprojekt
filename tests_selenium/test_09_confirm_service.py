from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import unittest
import testutils

#headless mode für chromedriver 
chrome_options = Options()
chrome_options.add_argument("--headless")

class register_login_test(unittest.TestCase):

    def setUp(self):
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def test_confirm_service(self):
        driver = self.driver
        testutils.login_customer(driver)
        assert "testkunde1@test.com" in driver.page_source
        testutils.confirm_service(driver)
        assert "Die Dienstleistung wurde abgenommen. Der Dienstleister kann den Auftrag nun abschließen." in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main(warnings='ignore')