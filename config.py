#!/usr/bin/env python3
"""
Module for the app configurations
"""
from os import getenv
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    MONGO_URI = "mongodb://{}:{}@{}:{}/{}".format(
        quote_plus(getenv('DB_USER')),
        quote_plus(getenv('DB_PASSWORD')),
        getenv('DB_HOST') or 'localhost',
        getenv('DB_PORT') or 27017,
        getenv('DB_NAME')
    )

    mongodb_details = {
        'db': getenv('DATABASE_USERNAME_DEV'),
        'host': getenv('DATABASE_PASSWORD'),
        'port': getenv('DATABASE_DEV')
    }


class TestingConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class DeploymentConfig(Config):
    pass


config = {
    'default': TestingConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'deployment': DeploymentConfig
}
