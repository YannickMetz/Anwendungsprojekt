from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os, pandas, lorem
from . forms import LoginForm, RegisterForm, ChangePasswordForm,LoadTestData
from . import db
from datetime import datetime
from .models import Dienstleister, Dienstleisterprofil, Dienstleistung, Kundenprofil, User, Kunde, Auftrag

mockdata = Blueprint('mockdata', __name__,template_folder='templates', static_folder='static')

def create_service(data_frame):
    for i in range(len(data_frame.index)):
        print(data_frame.iloc[:, 0][i])


def create_users_from_dataframe(data_frame, row_min, row_max, role):
    for i in range(row_max-row_min+1):
        
        user=User(
            email = data_frame["email"][row_min+i],
            password = generate_password_hash("test", method = 'pbkdf2:sha256', salt_length = 8),
            role = role
        )
        db.session.add(user)
        db.session.commit()

        if (role == "Kunde"):
            customer = Kunde(
                kunden_id = user.id,
                k_vorname = data_frame["first_name"][row_min+i],
                k_nachname = data_frame["last_name"][row_min+i],
                k_straße = f'{data_frame["street"][row_min+i]} {data_frame["street suffix"][row_min+i]} {data_frame["street number"][row_min+i]}',
                k_plz = data_frame["zip"][row_min+i],
                k_ort = data_frame["city"][row_min+i]
            )
            customer_profile=Kundenprofil(
                    kunden_id=user.id
            )
            db.session.add(customer)
            db.session.add(customer_profile)
            db.session.commit()
        
        elif (role == "Dienstleister"):
            service_provider = Dienstleister(
                    dienstleister_id = user.id,
                    d_vorname = data_frame["first_name"][row_min+i],
                    d_nachname = data_frame["last_name"][row_min+i],
                    firmenname = data_frame["company"][row_min+i],
                    d_straße = f'{data_frame["street"][row_min+i]} {data_frame["street suffix"][row_min+i]} {data_frame["street number"][row_min+i]}',
                    d_plz = data_frame["zip"][row_min+i],
                    d_ort = data_frame["city"][row_min+i],
                    radius = 30
            )
            service_provider_profile = Dienstleisterprofil (
                dienstleister_id = user.id,
                profilbeschreibung = lorem.paragraph()
            )
            db.session.add(service_provider)
            db.session.add(service_provider_profile)
            db.session.commit()



@mockdata.route('/load_mockdata', methods=['POST', 'GET'])
def load_mockdata():
    testdata_form=LoadTestData()
    if testdata_form.validate_on_submit():
        here=os.path.dirname(os.path.abspath(__file__))
        os.chdir(here)
        mock_data_frame = pandas.read_csv("MOCK_DATA.csv", sep=';')
        services = pandas.read_csv("services.csv", sep=';')
        create_service(services)

    return render_template("load_mockdata.html", form=testdata_form)

