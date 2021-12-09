from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from . forms import LoginForm, RegisterForm, ChangePasswordForm,LoadTestData
from . import db
from .models import User, Kunde

testdata = Blueprint('testdata', __name__,template_folder='templates', static_folder='static')


@testdata.route('/load_testdata', methods=['POST', 'GET'])
def load_testdata():
    testdata_form=LoadTestData()
    if testdata_form.validate_on_submit():
        test_user=User(
            email="2test@test.com",
            password=generate_password_hash(
                "1",
                method='pbkdf2:sha256',
                salt_length=8
            ),
            role = "Kunde"
        )
        db.session.add(test_user)
        db.session.commit()
        test_kunde=Kunde(
            kunden_id=test_user.id
        )
        db.session.add(test_kunde)
        db.session.commit()
        print(test_user)

        

    return render_template("load_testdata.html", form=testdata_form)

