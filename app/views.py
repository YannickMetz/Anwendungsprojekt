from posixpath import join
from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from sqlalchemy import dialects
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os, sys
from datetime import date
from . forms import AddProfileImageForm, ChangeProfileBodyForm, AddImageForm, SelectServiceForm, RequestQuotationForm
from . import db
from .models import User, Dienstleisterprofil, Auftrag, DienstleisterProfilGalerie, Dienstleistung, Dienstleister, Dienstleistung_Profil_association
from base64 import b64encode
from enum import Enum



views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

class ServiceOrderStatus(Enum):
    requested = "Übermittelt"
    rejected = "Abgelehnt"
    cancelled = "Storniert"
    quotation_available = "Angebot verfügbar"
    quotation_confirmed = "Angebot Bestätigt"
    service_confirmed = "Abgenommen"
    completed = "Abgeschlossen"

###### Functions ######

# erzeugt Dictionary mit den Dienstleistungen des Profils, welches aufsteigend nach Values (name der Dienstleistung) sortiert wird
def get_services_for_provider(id):
    services_query = Dienstleistung.query \
                        .join(Dienstleistung_Profil_association) \
                        .join(Dienstleister) \
                        .filter(Dienstleister.dienstleister_id == Dienstleistung_Profil_association.c.dienstleister_id) \
                        .where(Dienstleister.dienstleister_id == id)
    services_dict = {}
    for i in range(0,services_query.count()):
        services_dict.update({services_query[i].dienstleistung_id: services_query[i].Dienstleistung})
    services_dict=dict(sorted(services_dict.items(), key=lambda item: item[1],reverse=False))
    return services_dict



###### Routes ######

@views.route('/')
def home():
    categories_query = db.session.query(Dienstleistung.kategorieebene1).all()
    unique_categories = [i[0] for i in sorted(set(categories_query))]
    return render_template("index.html", categories=unique_categories)


@views.route('/change_service_provider_profile',methods=['POST', 'GET'])
@login_required
def change_service_provider_profile():
    current_profile = Dienstleisterprofil.query.filter_by(dienstleister_id=current_user.id).first()
    curren_service_provider = Dienstleister.query.filter_by(dienstleister_id=current_user.id).first()

    # erzeugt Dictionary mit Bilddateien aus der Datenbank für die Galerie des Profils
    gallery_table = DienstleisterProfilGalerie.query.filter_by(dienstleister_id=current_user.id).all()
    gallery_images = {}
    for i in range(0,len(gallery_table)):
        gallery_images.update({gallery_table[i].id: b64encode(gallery_table[i].galerie_bild).decode("utf-8")})

    # erzeugt Liste mit allen Dienstleistrungen aus der Datenbak
    all_services = Dienstleistung.query.all()
    services_list = []
    for service in all_services:
        services_list.append(service.Dienstleistung)
    services_list.sort()

    # erzeugt Dictionary mit den Dienstleistungen des Profils, welches aufsteigend nach Values (name der Dienstleistung) sortiert wird
    profile_services_dict = get_services_for_provider(current_user.id)

    # Profilbild zur Darstellung aus der Datenbank laden. 
    # Existiert das Bild nicht, wird ein Platzhalter aus dem static Verzeichnis geladen
    if current_profile.profilbild != None:
        profile_image = b64encode(current_profile.profilbild).decode('utf-8')
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, 'static/img/placeholder_flat.jpg')
        with open(filename, 'rb') as imagefile:
            profile_image = b64encode(imagefile.read()).decode('utf-8')

    # initialisierung der FlaskForms
    profile_image_form = AddProfileImageForm()
    profile_body_form = ChangeProfileBodyForm(profilbeschreibung=current_profile.profilbeschreibung)
    image_gallery_form = AddImageForm()
    service_form = SelectServiceForm()
    service_form.service.choices = services_list



    if profile_image_form.validate_on_submit():
        current_profile.profilbild = profile_image_form.profile_img.data.read()
        db.session.commit()
        return redirect(url_for('views.change_service_provider_profile'))

    if image_gallery_form.validate_on_submit():
        new_gallery_image = image_gallery_form.img.data.read()
        new_gallery_item= DienstleisterProfilGalerie(
            dienstleister_id = current_user.id,
            galerie_bild = new_gallery_image
        )
        db.session.add(new_gallery_item)
        db.session.commit()
        return redirect(url_for('views.change_service_provider_profile'))

    if service_form.validate_on_submit():
        try:
            curren_service_provider.relation.append(Dienstleistung.query.filter_by(Dienstleistung=service_form.service.data).first())
            db.session.commit()
        except:
            pass
        finally:
            return redirect(url_for('views.change_service_provider_profile'))

    if profile_body_form.validate_on_submit():
        current_profile.profilbeschreibung = profile_body_form.profilbeschreibung.data
        db.session.commit()
        return redirect(url_for('views.change_service_provider_profile'))

    return render_template(
        "change_business_profile.html",
        profile_image_form=profile_image_form,
        profile_body_form=profile_body_form,
        profile_image=profile_image,
        service_form=service_form,
        profile_services_dict=profile_services_dict,
        image_gallery_form=image_gallery_form,
        gallery_images=gallery_images
        )


@views.route('/profile/service_provider/<id>',methods=['POST', 'GET'])
@login_required
def view_service_provider_profile(id):

#dienstleister nach aufgerufener id
    service_provider = Dienstleister.query.where(Dienstleister.dienstleister_id == id).first()
    service_provider_id = service_provider.dienstleister_id

#vor, nachname und firmenname 
    service_provider_firstname = service_provider.d_vorname
    service_provider_lastname = service_provider.d_nachname
    service_provider_businessname = service_provider.firmenname

#dienstleistungen 
    services = Dienstleistung.query \
                        .join(Dienstleistung_Profil_association) \
                        .join(Dienstleister) \
                        .filter(Dienstleister.dienstleister_id == Dienstleistung_Profil_association.c.dienstleister_id) \
                        .where(Dienstleister.dienstleister_id == id) 

#dienstleisterprofil
    service_provider_profile = Dienstleisterprofil.query.where(Dienstleisterprofil.dienstleister_id == id).first()
    service_provider_profile_body = service_provider_profile.profilbeschreibung

#Bildergalerie
    gallery_table = DienstleisterProfilGalerie.query.filter_by(dienstleister_id=id).all()
    gallery_images = []
    for i in range(0,len(gallery_table)):
        gallery_images.append(b64encode(gallery_table[i].galerie_bild).decode("utf-8"))

#Profilbild
    if service_provider_profile.profilbild != None:
       service_provider_profile_image = b64encode(service_provider_profile.profilbild).decode('utf-8')
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, 'static/img/placeholder_flat.jpg')
        with open(filename, 'rb') as imagefile:
           service_provider_profile_image = b64encode(imagefile.read()).decode('utf-8')  

#übergabe in html code
    return render_template(
        "view_business_profile.html",
        service_provider_firstname = service_provider_firstname,
        service_provider_lastname = service_provider_lastname,
        service_provider_businessname = service_provider_businessname,
        service_provider_profile_image = service_provider_profile_image,
        service_provider_id = service_provider_id,
        services = services,
        gallery_images = gallery_images,
        service_provider_profile_body = service_provider_profile_body
        )


@views.route('/remove_service/<int:service_id>',methods=['POST', 'GET'])
@login_required
def remove_service(service_id):
    print(service_id)
    current_service_provider = Dienstleister.query.filter_by(dienstleister_id=current_user.id).first()
    current_service_provider.relation.remove(Dienstleistung.query.filter_by(dienstleistung_id=service_id).first())
    db.session.commit()
    return redirect(url_for('views.change_service_provider_profile'))


@views.route('/remove_gallery_image/<int:image_id>',methods=['POST', 'GET'])
@login_required
def remove_gallery_image(image_id):
    db.session.delete(DienstleisterProfilGalerie.query.filter_by(id=image_id).first())
    db.session.commit()

    return redirect(url_for('views.change_service_provider_profile'))


@views.route('/order/<id>', methods=['POST', 'GET'])
@login_required
def view_order(id):
    current_order = Auftrag.query.where(Auftrag.id == id).first()
    service = current_order.Dienstleistung_ID
    customer = current_order.Kunde_ID
    service_provider = current_order.Dienstleister_ID
    status = current_order.Status
    starttime = current_order.Startzeitpunkt
    endtime = current_order.Endzeitpunkt

    print(service, customer, service_provider, status, starttime, endtime)


@views.route('/search/<int:service_id>', methods=['GET'])
@login_required
def search_service(service_id):
    service_providers_filtered = Dienstleister.query \
        .join(Dienstleistung_Profil_association) \
        .join(Dienstleistung) \
        .filter(Dienstleistung.dienstleistung_id == Dienstleistung_Profil_association.c.dienstleistung_id) \
        .where(Dienstleistung.dienstleistung_id == service_id)

    service_providers_dict = {}
    for provider in service_providers_filtered:
        profile = Dienstleisterprofil.query.filter_by(dienstleister_id=provider.dienstleister_id).first()
        if profile.profilbild != None:
            service_providers_dict.update({provider: b64encode(profile.profilbild).decode("utf-8")})
        else:
            here = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(here, 'static/img/placeholder_flat.jpg')
            with open(filename, 'rb') as imagefile:
                service_providers_dict.update({provider: b64encode(imagefile.read()).decode('utf-8')})


    return render_template('search.html', service_providers = service_providers_dict)


@views.route('/search/<category1>', methods=['GET'])
@login_required
def select_service(category1):
    services = Dienstleistung.query.filter_by(kategorieebene1=category1).all()
    services_dict = {}
    for service in services:
        services_dict.update({service.dienstleistung_id: service.Dienstleistung})
    return render_template('services.html', services_dict=services_dict)


@views.route('/request-quotation/<id>', methods= ['GET', 'POST'])
@login_required
def request_quotation(id):

    services_dict = get_services_for_provider(id)
    services_list = [services_dict[service] for service in services_dict]

    quotation_form = RequestQuotationForm()
    quotation_form.service.choices = services_list

    if quotation_form.validate_on_submit():

        # stellt sicher, dass der Eintrag in der Datenbank auf 'NULL' gesetzt wird, falls kein Bild ausgewählt wurde 
        quotation_image = None 
        if quotation_form.img.data.headers['Content-Type'] != 'application/octet-stream':
            quotation_image = quotation_form.img.data.read()

        new_service_order = Auftrag(
            Dienstleistung_ID = quotation_form.service.data,
            Dienstleister_ID = id,
            anfrage_freitext = quotation_form.request.data,
            Startzeitpunkt = quotation_form.service_start.data,
            anfrage_bild = quotation_image,
            Status = ServiceOrderStatus.requested.value
        )
        db.session.add(new_service_order)
        db.session.commit()
        
        flash("Angebotsanfrage erfolgreich übermittelt.")
        return redirect(url_for('views.home'))


    return render_template('request-quotation.html', quotation_form=quotation_form, service_provider_id = id, services_list=services_list) 