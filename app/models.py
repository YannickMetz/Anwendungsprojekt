from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import relationship
from . import db
     
login_manager = LoginManager()

author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    
class Kunde(db.Model):
    __tablename__ = "Kunde"
    kunden_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    k_vorname = db.Column(db.String(20))
    k_nachname = db.Column(db.String(20))
    k_geburtstadum = db.Column(db.Date)
    k_straße = db.Column(db.String(20))
    k_plz = db.Column(db.String(20))
    k_ort = db.Column(db.String(20))

class Dienstleister(db.Model):
    __tablename__ = "Dienstleister"
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    d_vorname = db.Column(db.String(20))
    d_nachname = db.Column(db.String(20))
    firmenname = db.Column(db.String(20))
    d_geburtstadum = db.Column(db.Date)
    d_straße = db.Column(db.String(20))
    d_plz = db.Column(db.String(20))
    d_ort = db.Column(db.String(20))
    radius = db.Column(db.Integer)

class Dienstleistung(db.Model):
    __tablename__ = "Dienstleistung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Dienstleistung = db.Column(db.String(20))
    d_beschreibung = db.Column(db.String(100))

class Auftrag(db.Model):
    __tablename__ = "Auftrag"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Dienstleistung = db.Column(db.String(20), db.ForeignKey("Dienstleistung.id")) #FK aus Dienstleistung
    Kunde = db.Column(db.String(20), db.ForeignKey("Kunde.kunden_id")) #daten vom fk in tabelle holen? FK aus Kunde
    Dienstleister = db.Column(db.String(20), db.ForeignKey("Dienstleister.dienstleister_id")) #FK aus dienstleister
    Status = db.Column(db.String(20)) #Liste möglicher status festlegen
    Startzeitpunkt = db.Column(db.DateTime)
    Endzeitpunkt = db.Column(db.DateTime)
    Preis = db.Column(db.Numeric(precision=2))

class Dienstleistung_Profil(db.Model):
    __tablename__ = "Dienstleistung_Profil"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Dienstleister = db.Column(db.String(20), db.ForeignKey("Dienstleister.dienstleister_id")) #FK aus Dienstleister
    Dienstleistung = db.Column(db.String(20), db.ForeignKey("Dienstleistung.id")) #FK aus Dienstleistung

class Kundenbewertung(db.Model):
    __tablename__ = "Kundenbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    zahlungsverhalten = db.Column(db.Integer)

class Dienstleisterbewertung(db.Model):
    __tablename__ = "Dienstleisterbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    zufriedenheit = db.Column(db.Integer)

class Kundenprofil(db.Model):
    __tablename__ = "Kundenprofil"
    id = db.Column(db.Integer, db.ForeignKey("Kunde.kunden_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)
    bewertung = db.Column(db.Float, db.ForeignKey("Kundenbewertung.zahlungsverhalten"))

class Dienstleisterprofil(db.Model):
    __tablename__ = ("Dienstleisterprofil")
    id = db.Column(db.Integer, db.ForeignKey("Dienstleister.dienstleister_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)
    bewertung = db.Column(db.Float, db.ForeignKey("Dienstleisterbewertung.zufriedenheit"))
    dienstleistung = db.Column(db.String, db.ForeignKey("Dienstleistung_Profil.Dienstleistung_ID"))
    profilbeschreibung = db.Column(db.String)
    bildergalerie = db.Column(db.LargeBinary)