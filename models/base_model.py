#!/usr/bin/env python3
"""
Module for base model
"""
import uuid
import typing as t
from datetime import datetime
from mongoengine import (
    DateTimeField,
    StringField
)


class  BaseModel:
    """
    Class for the base model that other models can inherit from
    """
    id = StringField(required=True, primary_key=True, max_length=60)
    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = str(uuid.uuid4())

    def to_json(self) -> t.Dict[str, t.Any]:
        """
        Convert the document into a json
        """
        doc = vars(self)
        doc['created_at'] = self.created_at.isoformat()
        doc['updated_at'] = self.updated_at.isoformat()

        if 'password' in doc:
            del doc['password']

        return doc
