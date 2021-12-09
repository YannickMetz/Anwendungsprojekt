from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, URL, Optional




class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Passwort", validators=[DataRequired()])
    password_repeated = PasswordField(label="Passwort wiederholen", validators=[DataRequired()])
    role = SelectField(label="Kunde oder Dienstleister?", validators=[DataRequired()], choices=["Kunde", "Dienstleister"])
    submit = SubmitField("Registrierung absenden")

class ChangePasswordForm(FlaskForm):
    old_pw = PasswordField(label="Altes Passwort", validators=[DataRequired()])
    new_pw = PasswordField(label="Neues Passwort", validators=[DataRequired()])
    new_pw_repeated = PasswordField(label="Neues Passwort wiederholen", validators=[DataRequired()])
    submit = SubmitField("Passwortänderung übernehmen")


class LoadTestData(FlaskForm):
    submit = SubmitField("Lade Testdaten")