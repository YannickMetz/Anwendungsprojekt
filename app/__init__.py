from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from os import path
import os


db = SQLAlchemy()
DB_NAME = 'main_db.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "\xa5\x1d>\x8d9\x18@\xa1\xe9:\x07^\r\x81tP")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL_POSTGRESQL", f"sqlite:///{DB_NAME}") 
    # second argument fallback, if DB specified in environment variable is not available, for example on local machine.
    # when using heroku, cannot use the standard database variable. Create second variable in the heroku config with URL beginning updated from "postgres://" to "postgresql://"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .auth import auth
    from .views import views
    from .test_db_data import testdata
    from .mock_data import mockdata
    
    ckeditor = CKEditor(app)
    Bootstrap(app)
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(testdata)
    app.register_blueprint(mockdata)


    from .models import User, Kunde, Dienstleister, Dienstleisterbewertung, Kundenbewertung, Auftrag, Dienstleistung, Kundenprofil, Dienstleisterprofil, DienstleisterProfilGalerie

    create_database(app)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if app.config['SQLALCHEMY_DATABASE_URI'] == (f"sqlite:///{DB_NAME}"): # checks if the database URI points to a local SQLite databse
        if not path.exists(f'app/{DB_NAME}'):
            db.create_all(app=app)
            print('created database!')
    db.create_all(app=app)
