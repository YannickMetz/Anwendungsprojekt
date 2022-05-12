from selenium.webdriver.support.ui import Select

def register_customer(driver):
    driver.get('https://dienstleistung-on-demand.herokuapp.com')
    driver.find_element_by_id("register").click()
    #select funktion für dropdown menü
    Select(driver.find_element_by_id("role")).select_by_visible_text("Kunde")
    driver.find_element_by_id("submit").click()
    #registrierungsformular befüllen
    driver.find_element_by_id("k_vorname").send_keys("Max")
    driver.find_element_by_id("k_nachname").send_keys("Mustermann")
    driver.find_element_by_id("k_straße").send_keys("Musterstraße 13")
    driver.find_element_by_id("k_plz").send_keys("12345")
    driver.find_element_by_id("k_ort").send_keys("Musterstadt")
    driver.find_element_by_id("email").send_keys("testkunde1@test.com")
    driver.find_element_by_id("password").send_keys("test1234")
    driver.find_element_by_id("password_repeated").send_keys("test1234")
    driver.find_element_by_id("submit").click()

def register_service_provider(driver):
    driver.get('https://dienstleistung-on-demand.herokuapp.com')
    driver.find_element_by_id("register").click()
    #select funktion für dropdown menü
    Select(driver.find_element_by_id("role")).select_by_visible_text("Dienstleister")
    driver.find_element_by_id("submit").click()
    #registrierungsformular befüllen
    driver.find_element_by_id("d_vorname").send_keys("Max")
    driver.find_element_by_id("d_nachname").send_keys("Mustermann")
    driver.find_element_by_id("firmenname").send_keys("Musterfirma1 GmbH")
    driver.find_element_by_id("d_straße").send_keys("Musterstraße 13")
    driver.find_element_by_id("d_plz").send_keys("12345")
    driver.find_element_by_id("d_ort").send_keys("Musterstadt")
    driver.find_element_by_id("radius").send_keys("100")
    driver.find_element_by_id("email").send_keys("testdienstleister1@test.com")
    driver.find_element_by_id("password").send_keys("test1234")
    driver.find_element_by_id("password_repeated").send_keys("test1234")
    driver.find_element_by_id("submit").click()
