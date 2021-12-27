from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField
from wtforms import DateField, IntegerField
from wtforms.validators import DataRequired, URL, Optional
from flask_wtf.file import FileAllowed
from flask_ckeditor import CKEditorField

class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    role = SelectField(label="Kunde oder Dienstleister?", validators=[DataRequired()], choices=["Kunde", "Dienstleister"])
    submit = SubmitField("Registrierung fortsetzen")

class RegisterCustomerForm(FlaskForm):
    k_vorname = StringField(label="Vorname", validators=[DataRequired()])
    k_nachname = StringField(label="Nachname", validators=[DataRequired()])
    k_geburtstatum = DateField(label="Geburtsdatum (TT.MM.YYYY)", validators=[DataRequired()], format='%d.%m.%Y')
    k_straße = StringField(label="Straße und Hausnummer", validators=[DataRequired()])
    k_plz = StringField(label="Postleitzahl", validators=[DataRequired()])
    k_ort = StringField(label="Wohnort", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password_repeated = PasswordField(label="Passwort wiederholen", validators=[DataRequired()])
    submit = SubmitField("Registrierung abschließen")

class RegisterBusinessForm(FlaskForm):
    d_vorname = StringField(label="Vorname", validators=[DataRequired()])
    d_nachname = StringField(label="Nachname", validators=[DataRequired()]) 
    firmenname = StringField(label="Firmenname", validators=[DataRequired()])
    d_geburtstatum = DateField(label="Geburtsdatum (TT.MM.YYYY)", validators=[DataRequired()], format='%d.%m.%Y')
    d_straße = StringField(label="Straße und Hausnummer", validators=[DataRequired()])
    d_plz = StringField(label="Postleitzahl", validators=[DataRequired()])
    d_ort = StringField(label="Wohnort", validators=[DataRequired()])
    radius = IntegerField(label="Radius in dem sie Dienstleistungen anbieten möchten", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password_repeated = PasswordField(label="Passwort wiederholen", validators=[DataRequired()])
    submit = SubmitField("Registrierung abschließen")

class ChangePasswordForm(FlaskForm):
    old_pw = PasswordField(label="Altes Passwort", validators=[DataRequired()])
    new_pw = PasswordField(label="Neues Passwort", validators=[DataRequired()])
    new_pw_repeated = PasswordField(label="Neues Passwort wiederholen", validators=[DataRequired()])
    submit = SubmitField("Passwortänderung übernehmen")

class AddProfileImageForm(FlaskForm):
    profile_img = FileField("Bild auswählen", validators=[DataRequired(),FileAllowed(['jpg', 'jpeg'],'Only "jpg" and "jpeg" files are supported!')])
    submit_profile_img = SubmitField("Bild hochladen")

class AddImageForm(FlaskForm):
    img = FileField("Bild auswählen", validators=[DataRequired(),FileAllowed(['jpg', 'jpeg'],'Only "jpg" and "jpeg" files are supported!')])
    submit_img = SubmitField("Bild hochladen")

class ChangeProfileBodyForm(FlaskForm):
    profilbeschreibung = CKEditorField("Profilbeschreibung",validators=[DataRequired()])
    submit_body = SubmitField("Profilbeschreibung ändern")

class LoadTestData(FlaskForm):
    submit = SubmitField("Lade Testdaten")

class SelectServiceForm(FlaskForm):
    service = SelectField(label="Selektiere Dienstleistung", coerce=str, validators=[DataRequired()])
    submit_service = SubmitField("Dienstleistung hinzufügen")