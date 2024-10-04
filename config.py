#!/usr/bin/env python3
"""
Module for the app configurations
"""
from os import getenv
from datetime import timedelta
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    DB_HOST = getenv('DB_HOST') or 'localhost'
    DB_PORT = getenv('DB_PORT') or 27017
    DB_NAME = getenv('DB_NAME')
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=5)


class TestConfig(Config):
    pass


class DevConfig(Config):
    pass


class DeployConfig(Config):
    MONGO_URI = "mongodb://{}:{}@{}:{}/{}".format(
        quote_plus(getenv('DB_USER')),
        quote_plus(getenv('DB_PASSWORD')),
        getenv('DB_HOST') or 'localhost',
        getenv('DB_PORT') or 27017,
        getenv('DB_NAME')
    )


config = {
    'default': TestConfig,
    'test': TestConfig,
    'dev': DevConfig,
    'deploy': DeployConfig
}
