from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from . forms import LoginForm, RegisterForm
from . import db
from .models import User

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
        if User.query.filter_by(email=request.form.get('email')).first():
            #Benutzer existiert bereits
            flash("Account with this email adress already exists. Try login instead.")
            return redirect(url_for('auth.login'))
        new_user=User(
            email = register_form.email.data,
            password=generate_password_hash(
                register_form.password.data, 
                method='pbkdf2:sha256', 
                salt_length=8
            ),
            name = register_form.name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('views.timeline'))

    return render_template("register.html", form=register_form)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))