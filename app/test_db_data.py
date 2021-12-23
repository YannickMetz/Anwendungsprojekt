from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from . forms import LoginForm, RegisterForm, ChangePasswordForm,LoadTestData
from . import db
from .models import Dienstleister, Dienstleisterprofil, Dienstleistung, Kundenprofil, User, Kunde

testdata = Blueprint('testdata', __name__,template_folder='templates', static_folder='static')


@testdata.route('/load_testdata', methods=['POST', 'GET'])
def load_testdata():
    testdata_form=LoadTestData()
    if testdata_form.validate_on_submit():
        dienstleisterliste= []
        dienstleistungsliste= []

        for i in range(5):
        #testuser -> kunde    
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
                dienstleisterliste.append(test_dienstleister)

        #test dienstleisterprofil
                test_profil2=Dienstleisterprofil(
                    dienstleister_id=test_user2.id,
                    profilbeschreibung="ich kann alles machen"
                )
                db.session.add(test_profil2)
                db.session.commit()

        #test dienstleistung
        test_diensleistung1=Dienstleistung(
            kategorieebene1= "Körper",
            kategorieebene2= "Haare",
            Dienstleistung = "Friseur",
            d_beschreibung = "Haare schneiden"
        )
        test_diensleistung2=Dienstleistung(
            kategorieebene1= "Innen",
            kategorieebene2= "Boden",        
            Dienstleistung = "Fliesenleger",
            d_beschreibung = "Fliesen legen"
        )        
        test_diensleistung3=Dienstleistung(
            kategorieebene1= "Innen",
            kategorieebene2= "Wand",            
            Dienstleistung = "Tapezierer",
            d_beschreibung = "Wände tapezieren"
        )
        test_diensleistung4=Dienstleistung(
            kategorieebene1= "Außen",
            kategorieebene2= "Garten",            
            Dienstleistung = "Gärtner",
            d_beschreibung = "Garten erneuern"
        )
        test_diensleistung5=Dienstleistung(
            kategorieebene1= "Innen",
            kategorieebene2= "Elektronik",            
            Dienstleistung = "Elektriker",
            d_beschreibung = "Glühbirnen anbringen"
        )        
        db.session.add(test_diensleistung1)
        db.session.add(test_diensleistung2)
        db.session.add(test_diensleistung3)
        db.session.add(test_diensleistung4)
        db.session.add(test_diensleistung5)
        db.session.commit()
        dienstleistungsliste.append(test_diensleistung1)
        dienstleistungsliste.append(test_diensleistung2)
        dienstleistungsliste.append(test_diensleistung3)
        dienstleistungsliste.append(test_diensleistung4)
        dienstleistungsliste.append(test_diensleistung5)


        #dienstleistung und dienstleister in association table verknüpfen
        dienstleisterliste[0].relation.append(dienstleistungsliste[2])
        dienstleisterliste[0].relation.append(dienstleistungsliste[3])
        dienstleisterliste[0].relation.append(dienstleistungsliste[4])
        dienstleisterliste[2].relation.append(dienstleistungsliste[0])
        dienstleisterliste[2].relation.append(dienstleistungsliste[1])
        db.session.commit()

    return render_template("load_testdata.html", form=testdata_form)

