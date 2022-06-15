from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from . forms import LoginForm, RegisterForm, RegisterCustomerForm, ChangePasswordForm, RegisterBusinessForm
from . import db
from .models import Kunde, User, Dienstleister, Dienstleisterprofil

auth = Blueprint('auth', __name__,template_folder='templates', static_folder='static')



@auth.route('/login', methods=['POST', 'GET'])
def login():
    login_form=LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        #Email existiert nicht
        if user == None:
            flash("That email does not exist, please try again.")
            return redirect(url_for('auth.login'))
        #Passwort ist nicht korrekt
        elif check_password_hash(user.password, login_form.password.data) == False:
            flash('Password incorrect, please try again.')
            return redirect(url_for('auth.login'))
        #Email existiert und Passwort ist korrekt
        else:
            login_user(user)
            return redirect(url_for('views.home'))


    return render_template("login.html", form=login_form)



@auth.route('/register', methods=['POST', 'GET'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        if register_form.role.data == "Kunde":
            print("hello")
            return redirect(url_for('auth.register_customer'))
        elif register_form.role.data == "Dienstleister":
            return redirect(url_for('auth.register_business'))

    return render_template("register.html", form=register_form)



@auth.route('/register_customer', methods=['POST', 'GET'])
def register_customer():
    register_customer_form = RegisterCustomerForm()
    if register_customer_form.validate_on_submit():
        if User.query.filter_by(email=request.form.get('email')).first():
            #Benutzer existiert bereits
            flash("Es liegt bereits eine Registrierung mit dieser Email vor. Bitte Login probieren.")
            return redirect(url_for('auth.login'))
            
        if register_customer_form.password.data != register_customer_form.password_repeated.data:
            flash('Neue Passwörter stimmen nicht überein!')
            return redirect(url_for('auth.register_customer'))
            
        new_user=User(
            email = register_customer_form.email.data,
            password=generate_password_hash(
                register_customer_form.password.data, 
                method='pbkdf2:sha256', 
                salt_length=8
            ),
            role = "Kunde"
        )
        db.session.add(new_user)
        db.session.commit()

        new_kunde = Kunde(
            kunden_id=new_user.id,
            k_vorname = register_customer_form.k_vorname.data,
            k_nachname = register_customer_form.k_nachname.data,
            k_straße = register_customer_form.k_straße.data,
            k_plz = register_customer_form.k_plz.data,
            k_ort = register_customer_form.k_ort.data
        )
        db.session.add(new_kunde)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('views.home'))

    return render_template("register.html", form=register_customer_form)


@auth.route('/register_business', methods=['POST', 'GET'])
def register_business():
    register_business_form = RegisterBusinessForm()
    if register_business_form.validate_on_submit():
        if User.query.filter_by(email=request.form.get('email')).first():
            #Benutzer existiert bereits
            flash("Es liegt bereits eine Registrierung mit dieser Email vor. Bitte Login probieren.")
            return redirect(url_for('auth.login'))
    
        if register_business_form.password.data != register_business_form.password_repeated.data:
            flash('Neue Passwörter stimmen nicht überein!')
            return redirect(url_for('auth.register_business'))
        
        if Dienstleister.query.filter_by(firmenname=register_business_form.firmenname.data).first():
            flash('Firmenname wurde bereits registriert!')
            return redirect(url_for('auth.register_business'))

            
        new_user=User(
            email = register_business_form.email.data,
            password=generate_password_hash(
                register_business_form.password.data, 
                method='pbkdf2:sha256', 
                salt_length=8
            ),
            role = "Dienstleister"
        )
        db.session.add(new_user)
        db.session.commit()

        new_dienstleister = Dienstleister(
            dienstleister_id=new_user.id,
            d_vorname = register_business_form.d_vorname.data,
            d_nachname = register_business_form.d_nachname.data,
            firmenname = register_business_form.firmenname.data,
            #d_geburtstatum = register_business_form.d_geburtstatum.data,
            d_straße = register_business_form.d_straße.data,
            d_plz = register_business_form.d_plz.data,
            d_ort = register_business_form.d_ort.data,
            radius = register_business_form.radius.data
        )
        db.session.add(new_dienstleister)
        db.session.commit()

        new_dienstleister_profil = Dienstleisterprofil(dienstleister_id=new_user.id)
        db.session.add(new_dienstleister_profil)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('views.home'))

    return render_template("register.html", form=register_business_form)


@auth.route('/changepw', methods=['POST', 'GET'])
@login_required
def changepw():
    changepw_form = ChangePasswordForm()
    if changepw_form.validate_on_submit():
        user = current_user
        if check_password_hash(user.password, changepw_form.old_pw.data) == False:
            flash('Altes Passwort nicht korrekt!')
            return redirect(url_for('auth.changepw'))

        elif changepw_form.new_pw.data != changepw_form.new_pw_repeated.data:
            flash('Neue Passwörter stimmen nicht überein!')
            return redirect(url_for('auth.changepw'))

        elif check_password_hash(user.password, changepw_form.old_pw.data) == True:
            current_user.password = generate_password_hash(
                changepw_form.new_pw.data,
                method='pbkdf2:sha256', 
                salt_length=8
            )
            db.session.commit()
            return redirect(url_for('views.home'))
    
    return render_template("changepw.html", form=changepw_form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))