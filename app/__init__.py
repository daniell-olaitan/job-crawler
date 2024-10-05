#!/usr/bin/env python3
"""
Module to define the function to create the application instance
"""
from dotenv import load_dotenv
load_dotenv()

from models import db
from config import config
from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from mongoengine import connect

app_bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(app_env: str) -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[app_env])
    from app.v1.auth import auth
    from app.v1.app_views import app_views

    app.register_blueprint(auth)
    app.register_blueprint(app_views)
    app_bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={
        r'/v1*': {
            'origins': '*'
        }
    })

    if app_env in ['test', 'dev']:
        if app_env == 'dev':
            db.drop_database()

        connect(
            app.config['DB_NAME'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT']
        )
    else:
        connect(host=app.config['MONGO_URI'])

    return app
