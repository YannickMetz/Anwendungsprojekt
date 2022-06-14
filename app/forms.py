from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FileField, DecimalField, RadioField, BooleanField
from wtforms import DateField, IntegerField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, URL, Optional
from flask_wtf.file import FileAllowed
from wtforms import DateField
from flask_ckeditor import CKEditorField
from wtforms.widgets.core import CheckboxInput

# Klasse mit modifiziertem DecimalField, welches sowohl Komma als auch Punkt als Dezimaltrennzeichen erlaubt
class FlexibleDecimalField(DecimalField):
    def process_formdata(self, valuelist):
       if valuelist:
           valuelist[0] = valuelist[0].replace(",", ".")
       return super(FlexibleDecimalField, self).process_formdata(valuelist) 

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
    #k_geburtstatum = DateField(label="Geburtsdatum (TT.MM.YYYY)", validators=[DataRequired()], format='%d.%m.%Y')
    k_straße = StringField(label="Straße und Hausnummer", validators=[DataRequired()])
    k_plz = StringField(label="Postleitzahl", validators=[DataRequired()])
    k_ort = StringField(label="Wohnort", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password_repeated = PasswordField(label="Passwort wiederholen", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Registrierung abschließen")

class RegisterBusinessForm(FlaskForm):
    d_vorname = StringField(label="Vorname", validators=[DataRequired()])
    d_nachname = StringField(label="Nachname", validators=[DataRequired()]) 
    firmenname = StringField(label="Firmenname", validators=[DataRequired()])
    #d_geburtstatum = DateField(label="Geburtsdatum (TT.MM.YYYY)", validators=[DataRequired()], format='%Y-%m-%d')
    d_straße = StringField(label="Straße und Hausnummer", validators=[DataRequired()])
    d_plz = StringField(label="Postleitzahl", validators=[DataRequired()])
    d_ort = StringField(label="Wohnort", validators=[DataRequired()])
    radius = IntegerField(label="Radius in dem sie Dienstleistungen anbieten möchten", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password_repeated = PasswordField(label="Passwort wiederholen", validators=[DataRequired(), EqualTo('password')])
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

class RequestQuotationForm(FlaskForm):
    service = SelectField(label="Dienstleistung auswählen", coerce=str, validators=[DataRequired()])
    request = CKEditorField("Beschreiben sie ihre Anforderungen an den Dienstleister",validators=[DataRequired()])
    service_start = DateField(label="Wann soll die Dienstleistung beginnen?", format='%Y-%m-%d')
    img = FileField("Bild auswählen (Optional)", validators=[FileAllowed(['jpg', 'jpeg'],'Only "jpg" and "jpeg" files are supported!')])
    submit = SubmitField("Angebotsanfrage versenden")

class RateServiceForm(FlaskForm):
    rating = SelectField(label="Bitte bewerten Sie den Dienstleister mit einer Note (1 - Sehr schlecht bis 5 - Sehr gut)", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Abnahme und Bewertung bestätigen")

class CreateQuotation(FlaskForm):
    quote = FlexibleDecimalField(label="Bitte geben sie den Preis(€) für das Angebot ein:")
    service_finish = DateField(label="Bis wann kann die Dienstleistung erbacht werden?", format='%Y-%m-%d')
    submit = SubmitField("Angebot versenden")

class CancelOrder(FlaskForm):
    cancel_order = BooleanField(label = "Möchten sie den Auftrag stornieren?")
    submit_cancel_order = SubmitField("Bestätigen")

class AcceptQuotation(FlaskForm):
    accept_selection = RadioField('Label', choices=[('accept','akzeptieren'),('reject','ablehnen')])
    submit_accept = SubmitField("Akzeptieren")

class CompleteOrder(FlaskForm):
    complete_order = BooleanField(label = "Kunde hat Erfüllung der Dienstleistung bestätigt. Auftrag abschließen?")
    submit_complete_order = SubmitField("Bestätigen")

class SearchFilterForm(FlaskForm):
    service_date = DateField(label="Dienstleisterverfügbarkeit berücksichtigen", format='%Y-%m-%d')
    rating = SelectField(label="Bewertung mindestens (1 - schlecht bis 5 - Sehr gut):", coerce=int)
    submit_filter = SubmitField("Filter setzen")
