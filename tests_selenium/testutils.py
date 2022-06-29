from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time

def register_customer(driver):
    driver.get('http://127.0.0.1:5000/')
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

def register_service_provider(driver):
    driver.get('http://127.0.0.1:5000/')
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

def request_quotation_accept(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "Außen").click()
    driver.find_element(By.ID, "Garten").click()
    #Aufruf über XPATH da keine ID vergeben werden kann
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[5]/div/div/div[1]/a").click()
    driver.find_element(By.ID, "request_quotation").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Garten")
    #sleep um zu warten bis sich der iframe aufgebaut hat
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    #Aufruf über XPATH da keine ID vergeben werden kann, Eingabe in Textfeld
    driver.find_element(By.XPATH, "/html/body/p").send_keys("Wir möchten gerne einen Gärtner buchen.")
    driver.switch_to.default_content()
    #Datum im Datumsfeld eintragen 15.12.2023
    driver.find_element(By.ID, "service_start").send_keys("15122023")
    driver.find_element(By.ID, "submit").click()

def request_quotation_reject(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "Innen").click()
    driver.find_element(By.ID, "Möbelaufbau").click()
    #Aufruf über XPATH da keine ID vergeben werden kann
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/div/div/div[1]/a").click()
    driver.find_element(By.ID, "request_quotation").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Möbelaufbau")
    #sleep um zu warten bis sich der iframe aufgebaut hat
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    #Aufruf über XPATH da keine ID vergeben werden kann, Eingabe in Textfeld
    driver.find_element(By.XPATH, "/html/body/p").send_keys("Wir brauchen hilfe zum Möbelaufbau.")
    driver.switch_to.default_content()
    #Datum im Datumsfeld eintragen 15.12.2023
    driver.find_element(By.ID, "service_start").send_keys("15122023")
    driver.find_element(By.ID, "submit").click()

def request_quotation_confirm(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "Außen").click()
    driver.find_element(By.ID, "Fassade").click()
    #Aufruf über XPATH da keine ID vergeben werden kann
    driver.find_element(By.XPATH, "/html/body/div/div[2]/div[4]/div/div/div[1]/a").click()
    driver.find_element(By.ID, "request_quotation").click()
    Select(driver.find_element(By.ID, "service")).select_by_visible_text("Fassade")
    #sleep um zu warten bis sich der iframe aufgebaut hat
    time.sleep(3)
    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    #Aufruf über XPATH da keine ID vergeben werden kann, Eingabe in Textfeld
    driver.find_element(By.XPATH, "/html/body/p").send_keys("Wir brauchen hilfe bei unserere Fassade.")
    driver.switch_to.default_content()
    #Datum im Datumsfeld eintragen 15.12.2023
    driver.find_element(By.ID, "service_start").send_keys("15122023")
    driver.find_element(By.ID, "submit").click()

def create_quotation_accept(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    driver.find_element(By.ID, "Garten").click()
    driver.find_element(By.ID, "create_quotation").click()
    #Preis für den Auftrag festlegen, 300€
    driver.find_element(By.ID, "quote").send_keys("300")
    #Datum im Datumsfeld eintragen 01.02.2024
    driver.find_element(By.ID, "service_start").send_keys("02012023")
    driver.find_element(By.ID, "service_finish").send_keys("02012024")
    driver.find_element(By.ID, "submit").click()

def create_quotation_reject(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    driver.find_element(By.ID, "Möbelaufbau").click()
    driver.find_element(By.ID, "create_quotation").click()
    #Preis für den Auftrag festlegen, 300€
    driver.find_element(By.ID, "quote").send_keys("75")
    #Datum im Datumsfeld eintragen 01.02.2024
    driver.find_element(By.ID, "service_start").send_keys("02012023")
    driver.find_element(By.ID, "service_finish").send_keys("02012024")
    driver.find_element(By.ID, "submit").click()

def create_quotation_confirm(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    driver.find_element(By.ID, "Fassade").click()
    driver.find_element(By.ID, "create_quotation").click()
    #Preis für den Auftrag festlegen, 300€
    driver.find_element(By.ID, "quote").send_keys("1")
    #Datum im Datumsfeld eintragen 01.02.2024
    driver.find_element(By.ID, "service_start").send_keys("02012023")
    driver.find_element(By.ID, "service_finish").send_keys("02012024")
    driver.find_element(By.ID, "submit").click()
    
def accept_quotation_garten(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Garten").click()
    #angebot annehmen
    driver.find_element(By.ID, "accept_selection-0").click()
    driver.find_element(By.ID, "submit_accept").click()

def accept_quotation_fassade(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Fassade").click()
    #angebot annehmen
    driver.find_element(By.ID, "accept_selection-0").click()
    driver.find_element(By.ID, "submit_accept").click()

def reject_quotation(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Möbelaufbau").click()
    #angebot ablehnen
    driver.find_element(By.ID, "accept_selection-1").click()
    driver.find_element(By.ID, "submit_accept").click()

def cancel_order(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Garten").click()
    #angebot ablehnen
    driver.find_element(By.ID, "cancel_order").click()
    driver.find_element(By.ID, "submit_cancel_order").click()

def confirm_service(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Fassade").click()
    #angebot ablehnen
    driver.find_element(By.ID, "accept_quotation").click()
    #bewertung abgeben
    Select(driver.find_element(By.ID, "rating")).select_by_visible_text("4")
    driver.find_element(By.ID, "submit").click()

def complete_service(driver):
    driver.get('http://127.0.0.1:5000/')
    driver.find_element(By.ID, "actions").click()
    driver.find_element(By.ID, "show_orders").click()
    #Angebotsdetails öffnen
    driver.find_element(By.ID, "Fassade").click()
    driver.find_element(By.ID, "complete_order").click()
    driver.find_element(By.ID, "submit_complete_order").click()