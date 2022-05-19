from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import os
import time

def register_customer(driver):
    driver.get('http://127.0.0.1:5000/')
    time.sleep(10)
    driver.find_element(By.ID, "register").click()
    #select funktion für dropdown menü
    Select(driver.find_element(By.ID, "role")).select_by_visible_text("Kunde")
    driver.find_element(By.ID, "submit").click()
    #registrierungsformular befüllen
    driver.find_element(By.ID, "k_vorname").send_keys("Max")
    driver.find_element(By.ID, "k_nachname").send_keys("Mustermann")
    driver.find_element(By.ID, "k_straße").send_keys("Musterstraße 13")
    driver.find_element(By.ID, "k_plz").send_keys("12345")
    driver.find_element(By.ID, "k_ort").send_keys("Musterstadt")
    driver.find_element(By.ID, "email").send_keys("testkunde1@test.com")
    driver.find_element(By.ID, "password").send_keys("test1234")
    driver.find_element(By.ID, "password_repeated").send_keys("test1234")
    driver.find_element(By.ID, "submit").click()
    time.sleep(10)

def register_service_provider(driver):
    driver.get('http://127.0.0.1:5000/')
    time.sleep(10)
    driver.find_element(By.ID, "register").click()
    #select funktion für dropdown menü
    Select(driver.find_element(By.ID, "role")).select_by_visible_text("Dienstleister")
    driver.find_element(By.ID, "submit").click()
    #registrierungsformular befüllen
    driver.find_element(By.ID, "d_vorname").send_keys("Max")
    driver.find_element(By.ID, "d_nachname").send_keys("Mustermann")
    driver.find_element(By.ID, "firmenname").send_keys("Musterfirma1 GmbH")
    driver.find_element(By.ID, "d_straße").send_keys("Musterstraße 13")
    driver.find_element(By.ID, "d_plz").send_keys("12345")
    driver.find_element(By.ID, "d_ort").send_keys("Musterstadt")
    driver.find_element(By.ID, "radius").send_keys("100")
    driver.find_element(By.ID, "email").send_keys("testdienstleister1@test.com")
    driver.find_element(By.ID, "password").send_keys("test1234")
    driver.find_element(By.ID, "password_repeated").send_keys("test1234")
    driver.find_element(By.ID, "submit").click()

def login_customer(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "login").click()
    driver.find_element(By.ID, "email").send_keys("testkunde1@test.com")
    driver.find_element(By.ID, "password").send_keys("test1234")
    driver.find_element(By.ID, "submit").click()

def login_service_provider(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "login").click()
    driver.find_element(By.ID, "email").send_keys("testdienstleister1@test.com")
    driver.find_element(By.ID, "password").send_keys("test1234")
    driver.find_element(By.ID, "submit").click()
    
def add_service(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "change_profile").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Garten")
    driver.find_element(By.ID, "submit_service").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Fassade")
    driver.find_element(By.ID, "submit_service").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Möbelaufbau")
    driver.find_element(By.ID, "submit_service").click()

def request_quotation(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "Außen").click()
    driver.find_element(By.ID, "Winterdienst").click()
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div/div/div[1]/a").click()
    driver.find_element(By.ID, "request_quotation").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Winterdienst")
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    time.sleep(2)
    driver.find_element(By.XPATH, "/html/body/p").send_keys("Wir möchten gerne Winterdienst für unseren Hof buchen.")
    driver.switch_to.default_content()
    driver.find_element(By.ID, "service_start").send_keys("12152023")
    driver.find_element(By.ID, "submit").click()
    


    

