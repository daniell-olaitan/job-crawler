#!/usr/bin/env python3
"""
Module for user model
"""
from app import app_bcrypt
from models.parent_model import ParentModel
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)
from mongoengine import (
    Document,
    StringField,
    EmailField
)


class UserCreateValidator(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    password: str = Field(..., min_length=8)

    class Config:
        extra = 'forbid'


class UserLoginValidator(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

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
