#!/usr/bin/env python3
"""
Module to define the function to create the application instance
"""
from dotenv import load_dotenv
load_dotenv()

from models import db
import os
from config import config
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from mongoengine import connect
from flask_login import LoginManager
from flask_mail import Mail

app_bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
login_manager.login_view = 'auth.login'


def create_app(app_env: str) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[app_env])
    from app.auth import auth
    from app.job import job_views
    from app.user import user_views

    app.register_blueprint(auth)
    app.register_blueprint(job_views)
    app.register_blueprint(user_views)
    mail.init_app(app)
    app_bcrypt.init_app(app)
    login_manager.init_app(app)
    CORS(app)

    if not os.path.exists(app.config['RESUME_UPLOAD_FOLDER']):
        os.makedirs(app.config['RESUME_UPLOAD_FOLDER'])

    if not os.path.exists(app.config['IMAGE_UPLOAD_FOLDER']):
        os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'])

    if app_env in ['test', 'dev']:
        # if app_env == 'dev':
        #     db.drop_database()

        connect(
            app.config['DB_NAME'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT']
        )
    else:
        connect(host=app.config['MONGO_URI'])

    return app
