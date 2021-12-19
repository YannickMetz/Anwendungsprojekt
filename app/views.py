from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from datetime import date
from . forms import AddImageForm, ChangeProfileBodyForm
from . import db
from .models import User, Dienstleisterprofil
from base64 import b64encode


views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/change_business_profile',methods=['POST', 'GET'])
@login_required
def change_business_profile():
    current_profile = Dienstleisterprofil.query.filter_by(dienstleister_id=current_user.id).first()
    profile_image = b64encode(current_profile.profilbild).decode("utf-8") 

    profile_image_form = AddImageForm()
    if profile_image_form.validate_on_submit():
        current_profile.profilbild = profile_image_form.img.data.read()
        db.session.commit()
        return redirect(url_for('views.change_business_profile'))

    profile_body_form = ChangeProfileBodyForm(profilbeschreibung=current_profile.profilbeschreibung)
    if profile_body_form.validate_on_submit():
        current_profile.profilbeschreibung = profile_body_form.profilbeschreibung.data
        db.session.commit()
        return redirect(url_for('views.change_business_profile'))


    return render_template(
        "change_business_profile.html",
        profile_image_form=profile_image_form,
        profile_body_form=profile_body_form,
        profile_image=profile_image
        )
