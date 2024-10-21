#!/usr/bin/env python3
"""
Module for the app configurations
"""
from os import getenv
from urllib.parse import quote_plus


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    DB_HOST = getenv('DB_HOST') or 'localhost'
    DB_PORT = getenv('DB_PORT') or 27017
    DB_NAME = getenv('DB_NAME') or 'job_crawler_db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_SENDER = getenv('MAIL_SENDER')
    SECURITY_PASSWORD_SALT = getenv('SECURITY_PASSWORD_SALT')
    RESUME_UPLOAD_FOLDER = getenv('RESUME_UPLOAD_FOLDER')
    IMAGE_UPLOAD_FOLDER = getenv('IMAGE_UPLOAD_FOLDER')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


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
    'test': TestConfig,
    'dev': DevConfig,
    'deploy': DeployConfig
}
