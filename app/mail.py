import smtplib, ssl
from .classes import *
from email.mime.text import MIMEText as text
import os

# dictionary zum mappen von änderung des Auftraggsstatus und text der in der Email gesendet wird.
OrderActivies = {ServiceOrderStatus.requested: "Sie haben eien neuen Auftrag erhalten!\n",
                ServiceOrderStatus.rejected_by_customer: "Der Kunde hat den Auftrag abgelehnt!\n",
                ServiceOrderStatus.rejected_by_service_provider: "Der Dienstleister hat den Auftrag abgelehnt!\n",
                ServiceOrderStatus.quotation_available: "Der Dienstleister hat Ihnen ein Angebot erstellt!\n",
                ServiceOrderStatus.quotation_confirmed: "Der Kunde hat das Angebot bestätigt!\n",
                ServiceOrderStatus.service_confirmed: "Der Kunde hat bestätigt, dass die gewünschte Dienstleistung erbracht wurde!\n",
                ServiceOrderStatus.cancelled: "Ihr Auftrag wurde durch den Dienstleister storniert!\n",
                ServiceOrderStatus.completed: "Der Dienstleister hat den Auftrag abgeschlossen!\n"}

# definition der email funktion
def send_mail(receiver, status, order):
    #text für email
    message = text(OrderActivies[status] + "\nWeitere Informationen erhalten Sie in Ihrer Auftragsübersicht.")

    # [To] und ['Subject] mussten eingefügt werden da sonst nicht übernommen. Empfänger war in BCC und Betreff wurde nicht übernommen
    message['To'] = receiver
    message['Subject'] = "Dienstleistung on Demand - Auftragsabwicklung, Auftragsnummer: " + str(order.order_details.id)

    smtp_server = "smtp.gmail.com"
    # Port Für starttls
    port = 587
    sender_email = "dienstleistungondemand@gmail.com"
    #App-PW für gmail. Nicht zum login nutzbar. Aufgerufen über Umgebungsvariable
    password = os.environ["GMAILPW"]
    # Secure SSL context erstellen
    context = ssl.create_default_context()

    # serververbindung öffnen und email senden
    conn = smtplib.SMTP(smtp_server, port) 
    conn.ehlo()
    conn.starttls(context=context)
    conn.ehlo()
    conn.login(sender_email, password)
    conn.sendmail(sender_email, receiver, message.as_string())
 