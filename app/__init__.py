from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


db = SQLAlchemy()
DB_NAME = 'main_db.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xa5\x1d>\x8d9\x18@\xa1\xe9:\x07^\r\x81tP'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .auth import auth
    from .views import views
    

    Bootstrap(app)
    app.register_blueprint(auth)
    app.register_blueprint(views)

    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(f'app/{DB_NAME}'):
        db.create_all(app=app)
        print('created database!')
