#!/usr/bin/env python3
"""
Module for authentication
"""
from models import db
from models.user import User
import typing as t
from flask.typing import ResponseReturnValue

ModelType = t.TypeVar('Model')


class Auth:
    """
    Class for user authentication
    """

    def authenticate_user(self, **kwargs) -> ModelType:
        """
        Validate user login details
        """
        user = db.find(User, email=kwargs['email'])
        if user:
            if user.check_password(kwargs['password']):
                return user

            return None
        raise ValueError('email not registered')

    def register_user(
        self,
        **kwargs: t.Mapping
    ) -> ModelType:
        """
        Create and save a new user
        """
        user = db.find(User, email=kwargs['email'])
        if user:
            raise ValueError(f"User {kwargs['email']} already exists")

        user = db.insert(User, **kwargs)
        return user
