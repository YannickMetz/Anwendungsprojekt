import smtplib, ssl
from .forms import SendMail
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from . import db
from enum import Enum

mail = Blueprint('mail', __name__,template_folder='templates', static_folder='static')

class OrderActiviy(Enum):
    requested = "Sie haben eien neuen Auftrag erhalten!" # Kunde hat Angebot angefragt
    rejected_by_service_provider = "Abgelehnt durch Dienstleister" # Kunde hat Angebot abgeleht
    quotation_available = "Angebot verfügbar"
    rejected_by_customer = "Abgelehnt durch Kunde" # Kunde hat Angebot abgeleht
    quotation_confirmed = "Angebot bestätigt" # Kunde hat dem Angebot zugestimmt
    cancelled = "Storniert" # Durch Dienstleister. Nach verbindlicher Annahme kann der Auftrag nicht fortgeführt werden. 
    service_confirmed = "Abgenommen" # Kunde bestätigt, dass die geleistete Dienstleistung den Anforderungen entspricht
    completed = "Abgeschlossen" # Dienstleister hat Auftrag abgeschlossen

def send_mail(reciever, message):
    smtp_server = " smtp.web.de"
    port = 587  # For starttls
    sender_email = "dienstleistungondemand@gmail.com"
    password = "ELQPY754GLEEYLR5G7LK!"

    # Create a secure SSL context
    context = ssl.create_default_context()

    ## Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.connect
        server.ehlo()
        server.starttls(context=context) # Secure the connection
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, reciever, message)
    except Exception as e:
        # Print any error messages to stdout
        print("Error:", e)
    finally:
        server.quit() 
