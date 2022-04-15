from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os, pandas, lorem, random
from . forms import LoginForm, RegisterForm, ChangePasswordForm,LoadTestData
from . import db
from datetime import datetime, timedelta
from .models import Dienstleister, Dienstleisterbewertung, Dienstleisterprofil, Dienstleistung, Kundenprofil, User, Kunde, Auftrag
from .views import ServiceOrderStatus
from timeit import default_timer as timer
import click
from sqlalchemy import MetaData

mockdata = Blueprint('mockdata', __name__,template_folder='templates', static_folder='static')

@mockdata.cli.command("reset-db")
def reset_db():
    click.echo("Datenbank Reset beginnt...")
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        click.echo('Lösche Tabelle %s' % table)
        db.session.execute(table.delete())
    db.session.commit()


def create_service(data_frame):
    for i in range(len(data_frame.index)):
        service = Dienstleistung(
            kategorieebene1 = data_frame.iloc[:, 1][i],
            Dienstleistung = data_frame.iloc[:, 0][i]
        )
        db.session.add(service)
        db.session.commit()


def add_service(service_provider_id, service_id):
    Dienstleister.query.where(
        Dienstleister.dienstleister_id == service_provider_id
    ).first() \
    .relation.append(
        Dienstleistung.query.where(
            Dienstleistung.dienstleistung_id == service_id
            ).first()
    )
    db.session.commit()


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
                k_plz = int(data_frame["zip"][row_min+i]),
                k_ort = data_frame["city"][row_min+i]
            )
            customer_profile=Kundenprofil(
                    kunden_id=user.id
            )
            db.session.add(customer)
            db.session.add(customer_profile)
        
        elif (role == "Dienstleister"):
            service_provider = Dienstleister(
                    dienstleister_id = user.id,
                    d_vorname = data_frame["first_name"][row_min+i],
                    d_nachname = data_frame["last_name"][row_min+i],
                    firmenname = data_frame["company"][row_min+i],
                    d_straße = f'{data_frame["street"][row_min+i]} {data_frame["street suffix"][row_min+i]} {data_frame["street number"][row_min+i]}',
                    d_plz = int(data_frame["zip"][row_min+i]),
                    d_ort = data_frame["city"][row_min+i],
                    radius = 30
            )
            service_provider_profile = Dienstleisterprofil (
                dienstleister_id = user.id,
                profilbeschreibung = lorem.paragraph()
            )
            db.session.add(service_provider)
            db.session.add(service_provider_profile)
            services = list(data_frame["services"][row_min+i].split(','))
            for service in services:
                add_service(service_provider.dienstleister_id, int(service))

    db.session.commit()


def add_profile_image(service_provider_id, image_id):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, f'stock_images/{image_id}_stock.jpeg')
    profile = Dienstleisterprofil.query.where(
            Dienstleisterprofil.dienstleister_id == service_provider_id
            ) \
            .first()
    with open(filename, 'rb') as imagefile:
        profile.profilbild = imagefile.read()
    db.session.commit()


def create_service_orders(order_count, available_services, provider_lower, provider_upper, customer_lower, customer_upper):
    for order_id in range(0, order_count):
        start_date = datetime.now() - timedelta(weeks = random.randrange(1,12))
        end_date = start_date + timedelta(days = random.randrange(1,5))
        service_order = Auftrag(
            Dienstleistung_ID = random.randrange(1, available_services+1),
            Kunde_ID = random.randrange(customer_lower, customer_upper+1),
            Dienstleister_ID = random.randrange(provider_lower, provider_upper+1),
            anfrage_freitext = lorem.paragraph(),
            Startzeitpunkt = start_date,
            Endzeitpunkt = end_date, 
            Preis = random.randrange(100,1099),
            Status = ServiceOrderStatus.completed.value
        )
        db.session.add(service_order)
        db.session.commit()

        rating_value = int(random.randrange(1,6))
        rating = Dienstleisterbewertung(
            auftrags_ID = int(order_id),
            d_bewertung = rating_value
        )
        db.session.add(rating)
        db.session.commit()

    
@mockdata.cli.command("init-mockdata")
def init_mockdata():
    start = timer()
    #reset_db()
    click.echo("Lade testdaten...")
    here=os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)
    services = pandas.read_csv("services.csv", sep=';')
    mock_data_frame = pandas.read_csv("MOCK_DATA.csv", sep=';')
    click.echo("Füge Dienstleistungen hinzu...")
    create_service(services)
    click.echo("Pflege Benutzer (Dienstleister)...")
    create_users_from_dataframe(mock_data_frame, 0 , 20 ,"Dienstleister")
    click.echo("Pflege Benutzer (Kunden)...")
    create_users_from_dataframe(mock_data_frame, 21 , 500 ,"Kunde")
    click.echo("Lade Profilbilder...")
    add_profile_image(1,8)
    add_profile_image(2,6)
    add_profile_image(3,3)
    add_profile_image(4,1)
    add_profile_image(5,13)
    add_profile_image(6,9)
    add_profile_image(7,14)
    add_profile_image(8,15)
    add_profile_image(9,16)
    add_profile_image(10,4)
    add_profile_image(11,17)
    add_profile_image(12,10)
    # Kein Bild für ID 13
    add_profile_image(14,18)
    add_profile_image(15,11)
    add_profile_image(16,2)
    # Kein Bild für ID 17
    # Kein Bild für ID 18
    add_profile_image(19,19)
    # Kein Bild für ID 20
    # Kein Bild für ID 21
    create_service_orders(500,15,1,21,22,500)
    end = timer ()
    click.echo(f"Abgeschlossen.\nVergange Zeit: {end - start}")



