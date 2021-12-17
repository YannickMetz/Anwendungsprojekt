from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from . import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
     
login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    kunde_rel = relationship("Kunde", uselist=False, back_populates="user_rel")
    dienstleister_rel = relationship("Dienstleister", uselist=False, back_populates="user_rel")
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    
    
class Kunde(db.Model):
    __tablename__ = "Kunde"
    kunden_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    user_rel = relationship("User", back_populates="kunde_rel")
    k_vorname = db.Column(db.String(20))
    k_nachname = db.Column(db.String(20))
    k_geburtstatum = db.Column(db.Date)
    k_straße = db.Column(db.String(20))
    k_plz = db.Column(db.String(20))
    k_ort = db.Column(db.String(20))
    auftrag_rel = relationship("Auftrag")
    

class Dienstleister(db.Model):
    __tablename__ = "Dienstleister"
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    user_rel = relationship("User", back_populates="dienstleister_rel")
    d_vorname = db.Column(db.String(20))
    d_nachname = db.Column(db.String(20))
    firmenname = db.Column(db.String(20))
    d_geburtstatum = db.Column(db.Date)
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
    Dienstleistung_rel = relationship("Dienstleistung")
    Dienstleistung_ID = db.Column(db.String(20), db.ForeignKey("Dienstleistung.id")) #FK aus Dienstleistung
    Kunde_rel = relationship("Kunde")
    Kunde_ID = db.Column(db.String(20), db.ForeignKey("Kunde.kunden_id")) #FK aus Kunde
    Dienstleister_rel = relationship("Dienstleister")
    Dienstleister_ID = db.Column(db.String(20), db.ForeignKey("Dienstleister.dienstleister_id")) #FK aus dienstleister
    Status = db.Column(db.String(20)) #Liste möglicher status festlegen
    Startzeitpunkt = db.Column(db.DateTime)
    Endzeitpunkt = db.Column(db.DateTime)
    Preis = db.Column(db.Numeric(precision=2))

class Dienstleistung_Profil(db.Model):
    __tablename__ = "Dienstleistung_Profil"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Dienstleister_rel = relationship("Dienstleister")
    Dienstleister_ID = db.Column(db.String(20), db.ForeignKey("Dienstleister.dienstleister_id")) #FK aus Dienstleister
    Dienstleistung_rel = relationship("Dienstleistung")
    Dienstleistung_ID = db.Column(db.String(20), db.ForeignKey("Dienstleistung.id")) #FK aus Dienstleistung

association_table = ("association", Base.metadata, 
                    db.Column("Dienstleistung_Profil_ID", db.ForeignKey("Dienstleistung_Profil.id")), 
                    db.Column("Dienstleistung", db.ForeignKey("Dienstleistung_ID")))

class Kundenbewertung(db.Model):
    __tablename__ = "Kundenbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrag_rel = relationship("Auftrag")
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    zahlungsverhalten = db.Column(db.Integer)

class Dienstleisterbewertung(db.Model):
    __tablename__ = "Dienstleisterbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrag_rel = relationship("Auftrag")
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    zufriedenheit = db.Column(db.Integer)

class Kundenprofil(db.Model):
    __tablename__ = "Kundenprofil"
    id = db.Column(db.Integer, db.ForeignKey("Kunde.kunden_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)
    bewertung_rel = relationship("Kundenbewertung")
    bewertung = db.Column(db.Float, db.ForeignKey("Kundenbewertung.zahlungsverhalten"))

class Dienstleisterprofil(db.Model):
    __tablename__ = ("Dienstleisterprofil")
    dienstleister_rel = relationship("Dienstleister")
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("Dienstleister.dienstleister_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)
    bewertung_rel = relationship("Dienstleisterbewertung")
    bewertung = db.Column(db.Float, db.ForeignKey("Dienstleisterbewertung.zufriedenheit"))
    dienstleistung_rel = relationship("Dienstleistung_Profil")
    dienstleistung_ID = db.Column(db.String, db.ForeignKey("Dienstleistung_Profil.Dienstleistung_ID"))
    profilbeschreibung = db.Column(db.String)
    bildergalerie = db.Column(db.LargeBinary)