#!/usr/bin/env python3
"""
Module for invalid token model
"""
from models import db
from models.parent_model import ParentModel
from mongoengine import (
    Document,
    StringField,
)


class InvalidToken(ParentModel, Document):
    jti = StringField(required=True,  max_length=60)

    @classmethod
    def verify_jti(self, jti: str) -> bool:
        """
        Verify the JWT identity
        """
        return bool(db.find(self, jti=jti))
