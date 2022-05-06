from selenium import webdriver
import unittest

class dod_test(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(r"G:/SynologyDrive/Uni/7. Semester\Web-Technologie/Git-Repo/tests_selenium")
    
    def test_register_customer(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        register_button = driver.find_element_by_id("register")
        register_button.click
        role_dropdown = driver.find_element_by_id("role")
        role_dropdown.find_element_by_name("Kunde")
        role_dropdown.click
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "Vorname" in driver.page_source
        input_first_name = driver.find_element_by_id("k_vorname")
        input_first_name.send_keys("Max")
        input_last_name = driver.find_element_by_id("k_nachname")
        input_last_name.send_keys("Mustermann")
        input_street = driver.find_element_by_id("k_straße")
        input_street.send_keys("Musterstraße 13")
        input_zip_code = driver.find_element_by_id("k_plz")
        input_zip_code.send_keys("12345")
        input_city = driver.find_element_by_id("k_ort")
        input_city.send_keys("Musterstadt")
        input_email = driver.find_element_by_id("email")
        input_email.send_keys("testkunde100@test.com")
        input_pwd = driver.find_element_by_id("password")
        input_pwd.send_keys("test1234")
        input_rep_pwd = driver.find_element_by_id("password_repeated")
        input_rep_pwd.send_keys("test1234")
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "testkunde@test.com" in driver.page_source

    def test_register_service_provider(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        register_button = driver.find_element_by_id("register")
        register_button.click
        role_dropdown = driver.find_element_by_id("role")
        role_dropdown.find_element_by_name("Dienstleister")
        role_dropdown.click
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "Vorname" in driver.page_source
        input_first_name = driver.find_element_by_id("d_vorname")
        input_first_name.send_keys("Max")
        input_last_name = driver.find_element_by_id("d_nachname")
        input_last_name.send_keys("Mustermann")
        input_street = driver.find_element_by_id("d_straße")
        input_street.send_keys("Musterstraße 13")
        input_zip_code = driver.find_element_by_id("d_plz")
        input_zip_code.send_keys("12345")
        input_city = driver.find_element_by_id("d_ort")
        input_city.send_keys("Musterstadt")
        input_city = driver.find_element_by_id("radius")
        input_city.send_keys("100")
        input_email = driver.find_element_by_id("email")
        input_email.send_keys("testdienstleister100@test.com")
        input_pwd = driver.find_element_by_id("password")
        input_pwd.send_keys("test1234")
        input_rep_pwd = driver.find_element_by_id("password_repeated")
        input_rep_pwd.send_keys("test1234")
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "testdienstleister100@test.com" in driver.page_source

    def test_login_customer(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        login_button = driver.find_element_by_id("login")
        login_button.click
        input_email = driver.find_element_by_id("email")
        input_email.send_keys("testkunde@test.com")
        input_pwd = driver.find_element_by_id("password")
        input_pwd.send_keys("test1234")
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "testkunde@test.com" in driver.page_source

    def test_login_service_provider(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000')
        login_button = driver.find_element_by_id("login")
        login_button.click
        input_email = driver.find_element_by_id("email")
        input_email.send_keys("testdienstleister100@test.com")
        input_pwd = driver.find_element_by_id("password")
        input_pwd.send_keys("test1234")
        submit_button = driver.find_element_by_id("submit")
        submit_button.click
        assert "testdienstleister100@test.com" in driver.page_source


    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()