from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from . forms import LoginForm, RegisterForm, ChangePasswordForm,LoadTestData
from . import db
from .models import Dienstleister, Dienstleisterprofil, Dienstleistung, Kundenprofil, User, Kunde
from random_word import RandomWords

testdata = Blueprint('testdata', __name__,template_folder='templates', static_folder='static')


@testdata.route('/load_testdata', methods=['POST', 'GET'])
def load_testdata():
    testdata_form=LoadTestData()
    if testdata_form.validate_on_submit():
        #testuser -> kunde
        for i in range(5):
                test_user=User(
                    email=f"testkunde{i}@test.com",
                    password=generate_password_hash(
                        f"{i}",
                        method='pbkdf2:sha256',
                        salt_length=8),
                role = "Kunde"      
                )
                db.session.add(test_user)
                db.session.commit()
                #testkunde
                test_kunde=Kunde(
                    kunden_id=test_user.id,
                    k_vorname=f"testvorname{i}",
                    k_nachname=f"testnachname{i}",
                    k_straße="musterstraße 4",
                    k_plz="11111",
                    k_ort="Testhausen"
                )
                db.session.add(test_kunde)
                db.session.commit()

                #test kundenprofil
                test_profil=Kundenprofil(
                    kunden_id=test_user.id
                )
                db.session.add(test_profil)
                db.session.commit()

        #testuser -> dienstleister
                test_user2=User(
                    email=f"testdienstleister{i}@test.com",
                    password=generate_password_hash(
                        f"{i}",
                        method='pbkdf2:sha256',
                        salt_length=8
                    ),
                role = "Dienstleister"
                )
                db.session.add(test_user2)
                db.session.commit()
                #testdienstleister
                test_dienstleister=Dienstleister(
                    dienstleister_id=test_user2.id,
                    d_vorname=f"testvorname{i}",
                    d_nachname=f"testnachname{i}",
                    firmenname=f"testfirma{i}",
                    d_straße="musterstraße 4",
                    d_plz="11111",
                    d_ort="Testhausen",
                    radius=30
                    )
                db.session.add(test_dienstleister)
                db.session.commit()

                #test dienstleisterprofil
                test_profil2=Dienstleisterprofil(
                    dienstleister_id=test_user2.id,
                    profilbeschreibung="ich kann alles machen"
                )
                db.session.add(test_profil2)
                db.session.commit()

        #test dienstleistung
                test_diensleistung=Dienstleistung(
                    Dienstleistung = f"diensleistung{i}",
                    d_beschreibung = "sachen machen"
                )

            #dienstleistung und dienstleister in association table verknüpfen
                test_dienstleister.relation.append(test_diensleistung)
                db.session.add(test_diensleistung)
                db.session.commit()


    return render_template("load_testdata.html", form=testdata_form)

