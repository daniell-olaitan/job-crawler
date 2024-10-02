#!/usr/bin/env python3
"""
Module to define the function to create the application instance
"""
from dotenv import load_dotenv
load_dotenv()

from config import config
from flask import Flask
from flask_cors import CORS
from mongoengine import connect


def create_app(config_type: str = 'default') -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_type])
    from app.v1.auth import auth
    from app.v1.app_views import app_views

    app.register_blueprint(auth)
    app.register_blueprint(app_views)
    CORS(app, resources={
        r'/v1*': {
            'origins': '*'
        }
    })

    connect(host=config[config_type].MONGO_URI)
    return app
