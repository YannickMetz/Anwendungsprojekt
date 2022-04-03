import smtplib, ssl
from .classes import *
from . import db
from enum import Enum

OrderActivies = {ServiceOrderStatus.requested: "Sie haben eien neuen Auftrag erhalten!\n",
                 ServiceOrderStatus.cancelled: "Ihr Auftrag wurde abgebrochen" }

def send_mail(reciever, status, order):
    message = OrderActivies[status] + order.customer_contact
    
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "dienstleistungondemand@gmail.com"
    password = "zlybwbomapicvnrk"

    # Create a secure SSL context
    context = ssl.create_default_context()

    conn = smtplib.SMTP(smtp_server, port) 
    conn.ehlo()
    conn.starttls(context=context)
    conn.ehlo()
    conn.login(sender_email, password)
    conn.sendmail(sender_email, reciever, message)
 

# Yahoo APP PW: lfcqexqwrkchtctv!
# gmail APP PW: zlybwbomapicvnrk