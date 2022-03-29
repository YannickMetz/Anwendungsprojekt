from crypt import methods
import smtplib, ssl
from email.message import EmailMessage
from .views import ServiceOrder
from .models import Dienstleisterbewertung, User, Dienstleisterprofil, Auftrag, DienstleisterProfilGalerie, Dienstleistung, Dienstleister, Kunde, Dienstleistung_Profil_association
from .forms import SendMail
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from . import db

mail = Blueprint('mail', __name__,template_folder='templates', static_folder='static')

@mail.route('/send_mail/<id>', methods=['POST', 'GET'])
def get_contact(id):
    mail_form=SendMail()
    if mail_form.validate_on_submit:
        if current_user.role == "Dienstleister":
            current_order = ServiceOrder(id)
            receiver_email = current_order.service_provider_contact
            print(receiver_email)
        elif current_user.role == "Kunde":
            current_order = ServiceOrder(id)
            receiver_email = current_order.customer_contact
            print(receiver_email)

    return render_template(
        "send_mail.html",
        form=mail_form)


#smtp_server = "smtp.gmail.com"
#port = 587  # For starttls
#sender_email = "dienstleistungondemand@gmail.com"
#password = "G:\SynologyDrive\Uni\7. Semester\Web-Technologie\pw.txt"
#message = ""

# Create a secure SSL context
#context = ssl.create_default_context()
#
## Try to log in to server and send email
#try:
#    server = smtplib.SMTP(smtp_server,port)
#    server.starttls(context=context) # Secure the connection
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message)
#except Exception as e:
#    # Print any error messages to stdout
#    print(e)
#finally:
#    server.quit() 
