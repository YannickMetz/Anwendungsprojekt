from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from sqlalchemy.orm import relationship
from . import db
     
login_manager = LoginManager()



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    



