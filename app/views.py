from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from datetime import date
from . forms import AddProfileImageForm, ChangeProfileBodyForm, AddImageForm, SelectServiceForm
from . import db
from .models import User, Dienstleisterprofil, DienstleisterProfilGalerie, Dienstleistung, Dienstleister
from base64 import b64encode


views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/change_business_profile',methods=['POST', 'GET'])
@login_required
def change_business_profile():
    current_profile = Dienstleisterprofil.query.filter_by(dienstleister_id=current_user.id).first()
    curren_service_provider = Dienstleister.query.filter_by(dienstleister_id=current_user.id).first()

    gallery_table = DienstleisterProfilGalerie.query.filter_by(dienstleister_id=current_user.id).all()
    gallery_images = []
    for i in range(0,len(gallery_table)):
        gallery_images.append(b64encode(gallery_table[i].galerie_bild).decode("utf-8"))

    services = Dienstleistung.query.all()
    services_dict = {}
    for service in services:
        services_dict.update({service.dienstleistung_id: service.Dienstleistung})

    
    profile_image_form = AddProfileImageForm()
    profile_body_form = ChangeProfileBodyForm(profilbeschreibung=current_profile.profilbeschreibung)
    image_gallery_form = AddImageForm()
    service_form = SelectServiceForm()
    service_form.service.choices = list(services_dict.values())

    if current_profile.profilbild != None:
        profile_image = b64encode(current_profile.profilbild).decode('utf-8')
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(here, 'static/img/placeholder_flat.jpg')
        with open(filename, 'rb') as imagefile:
            profile_image = b64encode(imagefile.read()).decode('utf-8')


    if profile_image_form.validate_on_submit():
        current_profile.profilbild = profile_image_form.profile_img.data.read()
        db.session.commit()
        return redirect(url_for('views.change_business_profile'))

    if image_gallery_form.validate_on_submit():
        new_gallery_image = image_gallery_form.img.data.read()
        new_gallery_item= DienstleisterProfilGalerie(
            dienstleister_id = current_user.id,
            galerie_bild = new_gallery_image
        )
        db.session.add(new_gallery_item)
        db.session.commit()
        return redirect(url_for('views.change_business_profile'))

    if service_form.validate_on_submit():
        try:
            curren_service_provider.relation.append(Dienstleistung.query.filter_by(Dienstleistung=service_form.service.data).first())
            db.session.commit()
        except:
            pass
        finally:
            return redirect(url_for('views.change_business_profile'))

    if profile_body_form.validate_on_submit():
        current_profile.profilbeschreibung = profile_body_form.profilbeschreibung.data
        db.session.commit()
        return redirect(url_for('views.change_business_profile'))

    return render_template(
        "change_business_profile.html",
        profile_image_form=profile_image_form,
        profile_body_form=profile_body_form,
        profile_image=profile_image,
        service_form=service_form,
        image_gallery_form=image_gallery_form,
        gallery_images=gallery_images
        )
