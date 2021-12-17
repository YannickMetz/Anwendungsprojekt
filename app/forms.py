from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.fields.core import DateField, IntegerField
from wtforms.validators import DataRequired, URL, Optional




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


class LoadTestData(FlaskForm):
    submit = SubmitField("Lade Testdaten")