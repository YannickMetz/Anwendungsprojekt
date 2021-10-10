from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from datetime import date
from . forms import LoginForm, RegisterForm
from . import db
from .models import User
from base64 import b64encode


views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

@views.route('/')
def home():
    return render_template("index.html")

