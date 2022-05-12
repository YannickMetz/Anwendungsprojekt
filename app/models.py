from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import foreign
from . import db

login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    kunde_rel = relationship("Kunde", uselist=False, back_populates="user_rel")
    dienstleister_rel = relationship("Dienstleister", uselist=False, back_populates="user_rel")
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(100))
    
class Kunde(db.Model):
    __tablename__ = "Kunde"
    kunden_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    user_rel = relationship("User", back_populates="kunde_rel")
    k_vorname = db.Column(db.String(100))
    k_nachname = db.Column(db.String(100))
    k_geburtsdatum = db.Column(db.Date)
    k_straße = db.Column(db.String(100))
    k_plz = db.Column(db.String(100))
    k_ort = db.Column(db.String(100))
    auftrag_rel = relationship("Auftrag", back_populates="Kunde_rel")
    
Dienstleistung_Profil_association = db.Table("Dienstleistung_Profil", 
                                    db.Column("dienstleister_id", db.Integer, db.ForeignKey("Dienstleister.dienstleister_id")),
                                    db.Column("dienstleistung_id", db.Integer, db.ForeignKey("Dienstleistung.dienstleistung_id")),
                                    db.UniqueConstraint("dienstleister_id","dienstleistung_id")
                                    )
                                    
class Dienstleister(db.Model):
    __tablename__ = "Dienstleister"
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("User.id"), primary_key=True)
    user_rel = relationship("User", back_populates="dienstleister_rel")
    d_vorname = db.Column(db.String(100))
    d_nachname = db.Column(db.String(100))
    firmenname = db.Column(db.String(100))
    d_geburtstatum = db.Column(db.Date)
    d_straße = db.Column(db.String(100))
    d_plz = db.Column(db.String(100))
    d_ort = db.Column(db.String(100))
    radius = db.Column(db.Integer)
     
class Dienstleistung(db.Model):
    __tablename__ = "Dienstleistung"
    dienstleistung_id = db.Column(db.Integer, primary_key=True, unique=True)
    dienstleistung_profil_rel = db.relationship("Dienstleister", secondary=Dienstleistung_Profil_association, backref=db.backref("relation", lazy="dynamic"))
    kategorieebene1 = db.Column(db.String(100))
    kategorieebene2 = db.Column(db.String(100))
    Dienstleistung = db.Column(db.String(100))
    d_beschreibung = db.Column(db.String(100))

class Auftrag(db.Model):
    __tablename__ = "Auftrag"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    Dienstleistung_rel = relationship("Dienstleistung")
    Dienstleistung_ID = db.Column(db.Integer, db.ForeignKey("Dienstleistung.dienstleistung_id")) #FK aus Dienstleistung
    Kunde_rel = relationship("Kunde", back_populates="auftrag_rel")
    Kunde_ID = db.Column(db.Integer, db.ForeignKey("Kunde.kunden_id")) #FK aus Kunde
    Dienstleister_rel = relationship("Dienstleister")
    Dienstleister_ID = db.Column(db.Integer, db.ForeignKey("Dienstleister.dienstleister_id")) #FK aus dienstleister
    Status = db.Column(db.String(100)) #Liste möglicher status festlegen
    Startzeitpunkt = db.Column(db.DateTime)
    Endzeitpunkt = db.Column(db.DateTime)
    anfrage_freitext = db.Column(db.String(5000))
    anfrage_bild = db.Column(db.LargeBinary)
    Preis = db.Column(db.String(100))
    #Preis = db.Column(db.Numeric(precision=20, scale=2))

class Kundenbewertung(db.Model):
    __tablename__ = "Kundenbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrag_rel = relationship("Auftrag")
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    k_bewertung = db.Column(db.Integer)

class Dienstleisterbewertung(db.Model):
    __tablename__ = "Dienstleisterbewertung"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    auftrag_rel = relationship("Auftrag")
    auftrags_ID = db.Column(db.Integer, db.ForeignKey("Auftrag.id")) #FK von Auftrag
    d_bewertung = db.Column(db.Integer)

class Kundenprofil(db.Model):
    __tablename__ = "Kundenprofil"
    kunden_rel = relationship("Kunde")
    kunden_id = db.Column(db.Integer, db.ForeignKey("Kunde.kunden_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)


class Dienstleisterprofil(db.Model):
    __tablename__ = ("Dienstleisterprofil")
    dienstleister_rel = relationship("Dienstleister")
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("Dienstleister.dienstleister_id"), primary_key=True)
    profilbild = db.Column(db.LargeBinary)
    profilbeschreibung = db.Column(db.String(5000))
    bildergalerie_rel = relationship("DienstleisterProfilGalerie", back_populates="d_profil_rel")

class DienstleisterProfilGalerie(db.Model):
    __tablename__ = ("DienstleisterProfilGalerie")
    id = db.Column(db.Integer, primary_key=True)
    dienstleister_id = db.Column(db.Integer, db.ForeignKey("Dienstleisterprofil.dienstleister_id"))
    d_profil_rel = relationship("Dienstleisterprofil", back_populates="bildergalerie_rel")
    galerie_bild = db.Column(db.LargeBinary)

