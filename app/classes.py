from enum import Enum
from .models import Dienstleisterbewertung, User, Dienstleisterprofil, Auftrag, DienstleisterProfilGalerie, Dienstleistung, Dienstleister, Kunde, Dienstleistung_Profil_association
from base64 import b64encode

class ServiceOrderStatus(Enum):
    requested = "Übermittelt" # Kunde hat Angebot angefragt
    rejected_by_service_provider = "Abgelehnt durch Dienstleister" # Kunde hat Angebot abgeleht
    quotation_available = "Angebot verfügbar"
    rejected_by_customer = "Abgelehnt durch Kunde" # Kunde hat Angebot abgeleht
    quotation_confirmed = "Angebot bestätigt" # Kunde hat dem Angebot zugestimmt
    cancelled = "Storniert" # Durch Dienstleister. Nach verbindlicher Annahme kann der Auftrag nicht fortgeführt werden. 
    service_confirmed = "Abgenommen" # Kunde bestätigt, dass die geleistete Dienstleistung den Anforderungen entspricht
    completed = "Abgeschlossen" # Dienstleister hat Auftrag abgeschlossen

class ServiceOrder:
    def __init__(self, order_id):
        self.order_details = Auftrag.query.where(Auftrag.id == order_id).first()
        self.customer = Kunde.query.where(Kunde.kunden_id == self.order_details.Kunde_ID).first()
        self.service_provider = Dienstleister.query.where(Dienstleister.dienstleister_id == self.order_details.Dienstleister_ID).first()
        self.service = Dienstleistung.query.where(Dienstleistung.dienstleistung_id == self.order_details.Dienstleistung_ID).first()
        self.customer_contact = User.query.where(User.id == self.customer.kunden_id).first().email
        self.service_provider_contact = User.query.where(User.id == self.service_provider.dienstleister_id).first().email

        if Dienstleisterbewertung.query.where(Dienstleisterbewertung.auftrags_ID == order_id).first() != None:
            self.customer_rating = Dienstleisterbewertung.query.where(Dienstleisterbewertung.auftrags_ID == order_id).first().d_bewertung
        else:
            self.customer_rating = " "

        if self.order_details.Preis != None:
            self.quoted_price = str("{:.2f}".format(float(self.order_details.Preis)) + " €")
        else:
            self.quoted_price = "wird bearbeitet"
        if self.order_details.anfrage_bild != None:
            self.customer_image = b64encode(self.order_details.anfrage_bild).decode('utf-8')
        else:
            self.customer_image = None
