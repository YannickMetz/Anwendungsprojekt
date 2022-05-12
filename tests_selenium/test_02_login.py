from selenium import webdriver
import unittest
import os
import time
from testutils import register_customer

chromedriverpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "chromedriver.exe")

class register_login_test(unittest.TestCase):
    def setUp(self):
        #überprüfen ob chromedriver im pfad vorhanden ansonsten keine tests
        assert os.path.isfile(chromedriverpath) == True
        #driver für nachfolgende funktionen definieren
        self.driver = webdriver.Chrome(chromedriverpath)

    def test_login_customer(self):
        driver = self.driver
        register_customer(driver)
        driver.get('http://127.0.0.1:5000')
        driver.find_element_by_id("login").click
        driver.find_element_by_id("email").send_keys("testkunde1@test.com")
        driver.find_element_by_id("password").send_keys("test1234")
        driver.find_element_by_id("submit").click
        assert "testkunde1@test.com" in driver.page_source

    def test_login_service_provider(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        driver.find_element_by_id("login").click
        driver.find_element_by_id("email").send_keys("testdienstleister1@test.com")
        driver.find_element_by_id("password").send_keys("test1234")
        driver.find_element_by_id("submit").click
        assert "testdienstleister1@test.com" in driver.page_source

    def tearDown(self):
        time.sleep(5)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()