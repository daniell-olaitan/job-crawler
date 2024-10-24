#!/usr/bin/env python3
"""
Module for authentication
"""
from models import db
from models.user import User
import typing as t
from app import (
    mail,
    login_manager
)
from flask import render_template
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from flask import (
    current_app,
    flash,
    abort
)
from flask_login import (
    current_user,
    login_required
)
from functools import wraps
from flask.typing import ResponseReturnValue
from mongoengine import Document

ModelType = t.TypeVar('ModelType')


@login_manager.user_loader
def load_user(user_id: str) -> ModelType:
    """
    Load user
    """
    return db.find(User, id=user_id)


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
        raise ValueError('Email is not registered')

    def register_user(self, **kwargs: t.Mapping) -> ModelType:
        """
        Create and save a new user
        """
        user = db.find(User, email=kwargs['email'])
        if user:
            raise ValueError(f"User {kwargs['email']} already exists")

        return db.insert(User, **kwargs)

    def role_required(self, *roles: tuple) -> t.Callable:
        """
        Decorate a view function to require a role
        """
        def decorator(f: t.Callable) -> t.Callable:
            @wraps(f)
            def decorated_function(*args: t.Tuple, **kwargs: t.Mapping) -> ResponseReturnValue:
                if current_user.role not in roles:
                        flash("You don't have the permission to access the requested resource", 'error')
                        abort(403)

                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def login_required(self):
        """
        Decorator to check if the user is active and if the user is logged in
        """
        def decorator(f: t.Callable) -> t.Callable:
            @login_required
            @wraps(f)
            def decorated_function(*args: t.Tuple, **kwargs: t.Mapping) -> ResponseReturnValue:
                if current_user.status == 'inactive':
                    flash('Your account is being suspended', 'error')
                    abort(401)

                return f(*args, **kwargs)
            return decorated_function
        return decorator

    def send_reset_link(self, user: t.Type[Document]) -> None:
        """
        Send password reset link to user
        """
        token = self.generate_reset_token(user)
        msg = Message(
            subject='Reset Your Password',
            sender=current_app.config['MAIL_SENDER'],
            recipients=[user.email]
        )

        msg.body = render_template(
            'auth/password_reset_email.txt',
            user=user,
            token=token
        )

        mail.send(msg)

    def generate_reset_token(self, user: t.Type[Document]) -> str:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(user.id, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    def verify_reset_token(self, token: str, expiration: int = 600) -> str:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except Exception as err:
            return None

        return user_id
