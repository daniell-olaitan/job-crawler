#!/usr/bin/env python3
"""
Module to define the function to create the application instance
"""
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
from config import config
from flask import Flask
from flask_cors import CORS
from mongoengine import connect


def create_app(app_env: str = 'default') -> Flask:
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[app_env])
    from app.v1.auth import auth
    from app.v1.app_views import app_views

    app.register_blueprint(auth)
    app.register_blueprint(app_views)
    CORS(app, resources={
        r'/v1*': {
            'origins': '*'
        }
    })

    if app_env in ['test', 'dev']:
        DB_NAME = app.config['DB_NAME']
        DB_HOST = app.config['DB_HOST']
        DB_PORT = app.config['DB_PORT']

        client = MongoClient(DB_HOST, DB_PORT)
        db_list = client.list_database_names()

        if DB_NAME in db_list:
            client.drop_database(DB_NAME)

        connect(DB_NAME, host=DB_HOST, port=DB_PORT)
    else:
        connect(host=app.config['MONGO_URI'])

    return app
