from bz2 import compress
from flask import render_template, redirect, url_for, request, Blueprint, flash
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
from flask_login import login_required, current_user
import os
from datetime import date, datetime
from .mail import send_mail
from . forms import AddProfileImageForm, ChangeProfileBodyForm, AddImageForm, SelectServiceForm, RequestQuotationForm, CreateQuotation, SearchFilterForm, RateServiceForm, AcceptQuotation, CompleteOrder, CancelOrder, LoadTestData
from . import db
from .models import Dienstleisterbewertung, User, Dienstleisterprofil, Auftrag, DienstleisterProfilGalerie, Dienstleistung, Dienstleister, Dienstleistung_Profil_association
from base64 import b64encode
from .classes import *
from io import BytesIO
from PIL import Image

views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

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

def image_compressor(image):
    jpeg = Image.open(BytesIO(image))
    todb = BytesIO()
    jpeg.save(todb, format="JPEG" , quality=20)
    return todb.getvalue()

###### Routes ######

@views.route('/')
def home():
    categories_query = db.session.query(Dienstleistung.kategorieebene1).all()
    unique_categories = [i[0] for i in sorted(set(categories_query))]
    return render_template("index.html", categories=unique_categories)

@views.route('/change_service_provider_profile',methods=['POST', 'GET'])
@login_required
def change_service_provider_profile():
    user_role = User.query.filter_by(id=current_user.id).first().role
    if user_role == 'Kunde':
        flash('Bitte als Dienstleister einloggen')
        return redirect(url_for('auth.login'))

    elif user_role == 'Dienstleister':
        current_profile = Dienstleisterprofil.query.filter_by(dienstleister_id=current_user.id).first()
        current_service_provider = Dienstleister.query.filter_by(dienstleister_id=current_user.id).first()

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
            #print("hallo100")
        else:
            here = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(here, 'static/img/placeholder_flat.jpg')
            with open(filename, 'rb') as imagefile:
                profile_image = b64encode(imagefile.read())

        # initialisierung der FlaskForms
        profile_image_form = AddProfileImageForm()
        profile_body_form = ChangeProfileBodyForm(profilbeschreibung=current_profile.profilbeschreibung)
        image_gallery_form = AddImageForm()
        service_form = SelectServiceForm()
        service_form.service.choices = services_list

        if profile_image_form.validate_on_submit():
            current_profile.profilbild = profile_image_form.profile_img.data.read()
            #funktion wird doppelt ausgeführt?? print doppelt in shell
            #print("hallo bild hochgeladen")
            #try catch block für bild komprimierung von hochgeladenen bildern
            #try:
            current_profile.profilbild = image_compressor(current_profile.profilbild)
            #except Exception as e:
                #print("fehler!: " + str(e))
            
            db.session.commit()
            return redirect(url_for('views.change_service_provider_profile'))

        if image_gallery_form.validate_on_submit():
            new_gallery_image = image_gallery_form.img.data.read()
            #try catch block für bild komprimierung von hochgeladenen bildern
            ##try:
            new_gallery_item= DienstleisterProfilGalerie(
                dienstleister_id = current_user.id,
                galerie_bild = image_compressor(new_gallery_image))
            #except Exception as e:  
                #print("fehler!: " + str(e))

            db.session.add(new_gallery_item)
            db.session.commit()
            return redirect(url_for('views.change_service_provider_profile'))

        if service_form.validate_on_submit():
            try:
                current_service_provider.relation.append(Dienstleistung.query.filter_by(Dienstleistung=service_form.service.data).first())
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

    #bewertung auslesen
    ratings = Dienstleisterbewertung.query \
                .join(Auftrag) \
                .join(Dienstleister) \
                .filter(Auftrag.Dienstleister_ID == Dienstleister.dienstleister_id) \
                .filter(Dienstleisterbewertung.auftrags_ID == Auftrag.id) \
                .where(Dienstleister.dienstleister_id == id)

    rating_values = [rating.d_bewertung for rating in ratings] 
    if len(rating_values) == 0:
         rating_values = None
         rating_average = "Keine Bewertung vorhanden"
    else:
        rating_average = sum(rating_values) / len(rating_values)
        rating_average = f"{rating_average: .2f}"

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
        service_provider_profile_body = service_provider_profile_body,
        rating_average = rating_average
        )

@views.route('/remove_service/<int:service_id>',methods=['POST', 'GET'])
@login_required
def remove_service(service_id):
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

@views.route('/orders/', methods=['POST', 'GET'])
@login_required
def view_order():
    
    if current_user.role == "Dienstleister":
        open_orders = Auftrag.query.where(Auftrag.Dienstleister_ID == current_user.id).filter \
                        (or_(Auftrag.Status == ServiceOrderStatus.requested.value, \
                        Auftrag.Status == ServiceOrderStatus.quotation_available.value, \
                        Auftrag.Status == ServiceOrderStatus.service_confirmed.value, \
                        Auftrag.Status == ServiceOrderStatus.quotation_confirmed.value)).all()

        closed_orders = Auftrag.query.where(Auftrag.Dienstleister_ID == current_user.id).filter \
                        (or_(Auftrag.Status == ServiceOrderStatus.completed.value, \
                        Auftrag.Status == ServiceOrderStatus.rejected_by_customer.value, \
                        Auftrag.Status == ServiceOrderStatus.cancelled.value, \
                        Auftrag.Status == ServiceOrderStatus.rejected_by_service_provider.value)).all()

    elif current_user.role == "Kunde":
        open_orders = Auftrag.query.where(Auftrag.Kunde_ID == current_user.id).filter \
                        (or_(Auftrag.Status == ServiceOrderStatus.requested.value, \
                        Auftrag.Status == ServiceOrderStatus.quotation_available.value, \
                        Auftrag.Status == ServiceOrderStatus.service_confirmed.value, \
                        Auftrag.Status == ServiceOrderStatus.quotation_confirmed.value)).all()

        closed_orders = Auftrag.query.where(Auftrag.Kunde_ID == current_user.id).filter \
                        (or_(Auftrag.Status == ServiceOrderStatus.completed.value, \
                        Auftrag.Status == ServiceOrderStatus.rejected_by_customer.value, \
                        Auftrag.Status == ServiceOrderStatus.cancelled.value, \
                        Auftrag.Status == ServiceOrderStatus.rejected_by_service_provider.value)).all()

    service_orders_open = []
    for order in open_orders:
        my_open_order = ServiceOrder(order.id)
        service_orders_open.append(my_open_order)

    service_orders_closed = []
    for order in closed_orders:
        my_closed_order = ServiceOrder(order.id)
        service_orders_closed.append(my_closed_order)

    return render_template(
            "view_order.html",
            service_orders_open = service_orders_open,
            service_orders_closed = service_orders_closed
            )

@views.route('/search/<int:service_id>', methods=['GET', 'POST'])
@login_required
def search_service_providers(service_id):

    query_params = request.args.to_dict()
    if len(query_params) == 0:
        filter_date = datetime(1970,1,1)
        filter_rating = 0
    else:
        filter_date = datetime.strptime(query_params['date'],"%Y-%m-%d")
        filter_rating = int(query_params['rating'])
    
    subquery_date = db.session.query(Auftrag.Dienstleister_ID).filter(
            (filter_date >= Auftrag.Startzeitpunkt_Kunde) &
            (filter_date <= Auftrag.Endzeitpunkt)
        ).subquery()
    
    subquery_score = db.session.query(Dienstleister.dienstleister_id) \
        .join(Auftrag, Dienstleister.dienstleister_id==Auftrag.Dienstleister_ID)\
        .join(Dienstleisterbewertung, Auftrag.id==Dienstleisterbewertung.auftrags_ID)\
        .group_by(Dienstleister.dienstleister_id)\
        .having(func.avg(Dienstleisterbewertung.d_bewertung)>=filter_rating).subquery()
    
    if len(query_params) == 0:
        service_providers_filtered = Dienstleister.query \
            .join(Dienstleistung_Profil_association) \
            .join(Dienstleistung) \
            .filter(Dienstleistung.dienstleistung_id == Dienstleistung_Profil_association.c.dienstleistung_id) \
            .where(Dienstleistung.dienstleistung_id == service_id)
    else:
        service_providers_filtered = Dienstleister.query \
            .join(Dienstleistung_Profil_association) \
            .join(Dienstleistung) \
            .filter(Dienstleistung.dienstleistung_id == Dienstleistung_Profil_association.c.dienstleistung_id) \
            .where(
                (Dienstleistung.dienstleistung_id == service_id)&
                (Dienstleister.dienstleister_id.not_in(subquery_date))&
                (Dienstleister.dienstleister_id.in_(subquery_score))
                )

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

    if len(query_params) == 0:
        filter_date = date.today()
    ratings = [0,1,2,3,4,5]
    search_filter_form = SearchFilterForm(service_date=filter_date)
    search_filter_form.rating.choices = ratings
    if search_filter_form.validate_on_submit():
        filter_date = search_filter_form.service_date.data
        filter_rating = search_filter_form.rating.data
        return redirect(url_for('views.search_service', service_id=service_id, date=[filter_date], rating=[filter_rating]))

    return render_template('search.html', service_providers = service_providers_dict, search_filter_form=search_filter_form)

@views.route('/search/<category1>', methods=['GET'])
@login_required
def view_services(category1):
    services = Dienstleistung.query.filter_by(kategorieebene1=category1).all()
    services_dict = {}
    for service in services:
        services_dict.update({service.dienstleistung_id: service.Dienstleistung})
    return render_template('services.html', services_dict=services_dict)

@views.route('/request-quotation/<int:id>', methods= ['GET', 'POST'])
@login_required
def request_quotation(id):
    
    if current_user.role == "Dienstleister":
        flash("Sie können als Dienstleister leider keine Dienstleistungen anfragen.")
        return redirect(url_for('views.home'))

    services_dict = get_services_for_provider(id)
    services_list = [services_dict[service] for service in services_dict]

    quotation_form = RequestQuotationForm()
    quotation_form.service.choices = services_list

    if quotation_form.validate_on_submit():

        # stellt sicher, dass der Eintrag in der Datenbank auf 'NULL' gesetzt wird, falls kein Bild ausgewählt wurde 
        quotation_image = None 
        if quotation_form.img.data.headers['Content-Type'] != 'application/octet-stream':
            quotation_image = image_compressor(quotation_form.img.data.read())
        
        new_service_order = Auftrag(
            Dienstleistung_ID = list(services_dict.keys())[list(services_dict.values()).index(quotation_form.service.data)],
            Kunde_ID = current_user.id,
            Dienstleister_ID = id,
            anfrage_freitext = quotation_form.request.data,
            Startzeitpunkt_Kunde = quotation_form.service_start.data,
            anfrage_bild = quotation_image,
            Status = ServiceOrderStatus.requested.value
        )
        db.session.add(new_service_order)
        db.session.commit()

        #Empfänger Email herausfinden + email senden
        open_order = ServiceOrder(new_service_order.id)
        receiver = open_order.service_provider_contact
        send_mail(receiver, ServiceOrderStatus.requested, open_order)

        flash("Angebotsanfrage erfolgreich übermittelt.")
        return redirect(url_for('views.home'))

    return render_template(
        'request-quotation.html',
        quotation_form=quotation_form,
        service_provider_id = id,
        services_list=services_list
        )

@views.route('/order-details/<id>', methods=['GET','POST'])
@login_required
def view_order_details(id):
    service_order = ServiceOrder(id)

    #quotation_button = ProcessQuotation()
    accept_radio = AcceptQuotation()
    cancel_checkbox = CancelOrder()
    complete_checkbox = CompleteOrder()

    if accept_radio.validate_on_submit():
        if accept_radio.accept_selection.data == 'accept':
            service_order.order_details.Status = ServiceOrderStatus.quotation_confirmed.value
            db.session.commit()
            flash("Angebot angenommen.")
            #Empfänger Email herausfinden + email senden
            receiver = service_order.service_provider_contact
            send_mail(receiver, ServiceOrderStatus.quotation_confirmed, service_order)
            return redirect(url_for('views.view_order_details', id=id))
        elif accept_radio.accept_selection.data == 'reject':
            service_order.order_details.Status = ServiceOrderStatus.rejected_by_customer.value
            db.session.commit()
            #Empfänger Email herausfinden + email senden
            receiver = service_order.service_provider_contact
            send_mail(receiver, ServiceOrderStatus.rejected_by_customer, service_order)
            flash("Angebot wurde abgelehnt.")
            return redirect(url_for('views.view_order_details', id=id))

    if cancel_checkbox.validate_on_submit():
        if cancel_checkbox.cancel_order.data == True:
            service_order.order_details.Status = ServiceOrderStatus.cancelled.value
            db.session.commit()
            #Empfänger Email herausfinden + email senden
            receiver = service_order.customer_contact
            send_mail(receiver, ServiceOrderStatus.cancelled, service_order)
            flash("Auftrag erfolgreich storniert.")
            return redirect(url_for('views.view_order'))

    if complete_checkbox.validate_on_submit():
        if complete_checkbox.complete_order.data == True:
            service_order.order_details.Status = ServiceOrderStatus.completed.value
            db.session.commit()
            flash("Auftrag erfolgreich beendet.")
            return redirect(url_for('views.view_order'))

    return render_template('order-details.html', 
        service_order=service_order,
        accept_radio=accept_radio,
        cancel_checkbox=cancel_checkbox,
        complete_checkbox=complete_checkbox,
        ServiceOrderStatus=ServiceOrderStatus
        )

@views.route('/confirm_order/<id>', methods=['POST', 'GET'])
@login_required
def confirm_order(id):
    confirm_order = ServiceOrder(id)
    rating_choices = [5,4,3,2,1]
    confirm_form = RateServiceForm()
    confirm_form.rating.choices = rating_choices

    if confirm_form.validate_on_submit():
        print(confirm_form.rating.data)
        rating = Dienstleisterbewertung(
            auftrags_ID = confirm_order.order_details.id,
            d_bewertung = confirm_form.rating.data)
        db.session.add(rating)
        db.session.commit() 
        confirm_order.order_details.Status = ServiceOrderStatus.service_confirmed.value
        db.session.commit()

        #Empfänger Email herausfinden + email senden
        receiver = confirm_order.service_provider_contact
        send_mail(receiver, ServiceOrderStatus.service_confirmed, confirm_order)

        flash("Die Dienstleistung wurde abgenommen. Der Dienstleister kann den Auftrag nun abschließen..")
        return redirect(url_for('views.view_order_details', id=id)) 

    return render_template(
        'confirm_order.html',
        confirm_order = confirm_order,
        confirm_form = confirm_form
        )

@views.route('/quote/<id>', methods=['POST', 'GET'])
@login_required
def create_quotation(id):
    service_order = ServiceOrder(id)
    quotation_form = CreateQuotation()
    if quotation_form.validate_on_submit():
        quotation_price = str(round(quotation_form.quote.data, 2))
        #start und endzeitpunkt für die erbringung der dienstleistung
        service_start = quotation_form.service_start.data
        service_finish = quotation_form.service_finish.data
        service_order.order_details.Status = ServiceOrderStatus.quotation_available.value
        service_order.order_details.Preis = quotation_price
        service_order.order_details.Startzeitpunkt_Dienstleister = service_start
        service_order.order_details.Endzeitpunkt = service_finish
        #überprüfung ob endzeitpunkt nach startzeitpunk und ob startzeitpunkt nich älter als aktuelles datum ist
        if service_finish < service_start:
            flash('Der Endzeitpunkt kann nicht vor dem Startzeitpunkt liegen!')
            return redirect(url_for('views.create_quotation', id=id))
        elif service_start < date.today():
            flash('Der Startzeitpunkt kann nicht in der Vergangenheit liegen!')
            return redirect(url_for('views.create_quotation', id=id))
        else:
            db.session.commit()
            #Empfänger Email herausfinden + email senden
            receiver = service_order.customer_contact
            send_mail(receiver, ServiceOrderStatus.quotation_available, service_order)
            return redirect(url_for('views.view_order_details', id=id))

    return render_template('quote.html', service_order=service_order, quotation_form=quotation_form)


@views.route('/jpeg', methods =['POST','GET'])
def get_jpeg_files():
    form = LoadTestData()

    return render_template('load_testdata.html', form=form)
