# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager, current_user
from .models.user import User
from .models.picture import Picture
from .models.folder import Folder
from .models.database import session

from .config.config import CONNECT_STR

from flask_admin.contrib.sqla import ModelView

mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = 'here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sdsgoubmroepjg:bea71326aeb64aa1a2675b5e2f895b7a2ef59017a29ed16ab8b4a2acf9558e43@ec2-54-161-189-150.compute-1.amazonaws.com:5432/dafcbomp5q6jqs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/images'
    app.config['MAIL_SERVER'] = 'mail74.onamae.ne.jp'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'info@keigonomura.com'
    app.config['MAIL_PASSWORD'] = 'KeigoUWC0126!'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail.init_app(app)    

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app