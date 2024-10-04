#!/usr/bin/env python3
"""
Module for user model
"""
from app import app_bcrypt
from models.parent_model import ParentModel
from pydantic import (
    BaseModel,
    EmailStr
)
from mongoengine import (
    Document,
    StringField,
    EmailField
)


class UserCreateValidator(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        extra = 'forbid'


class UserLoginValidator(BaseModel):
    email: EmailStr
    password: str

    class Config:
        extra = 'forbid'


class User(ParentModel, Document):
    first_name = StringField(required=True, max_length=60)
    last_name = StringField(required=True, max_length=60)
    email = EmailField(required=True, unique=True, max_length=60)
    password = StringField(required=True, max_length=60)

    def pre_save(self):
        self.password = app_bcrypt.generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password):
        return app_bcrypt.check_password_hash(self.password, password)
