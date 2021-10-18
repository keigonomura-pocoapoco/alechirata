# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager, current_user
from .models.user import User
from .models.picture import Picture
from .models.folder import Folder
from .models.database import session

from datetime import timedelta

from .config.config import CONNECT_STR

from flask_admin.contrib.sqla import ModelView

mail = Mail()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = 'here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ejvchrmncdntmt:a46905a0329423170a3da2c4e937f57f1590ac3cfcff3d8daed25278606e64b5@ec2-54-145-188-92.compute-1.amazonaws.com:5432/d634oto7gkjca'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
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