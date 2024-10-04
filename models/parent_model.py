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


class  ParentModel:
    """
    Class for the base model that other models can inherit from
    """
    id = StringField(primary_key=True, max_length=60, default=lambda: str(uuid.uuid4()))
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def pre_save(self):
        """
        Override the pre_save method to transform data before saving, e.g password hashing.
        This method will only be called when the document is newly created.
        """
        pass

    def to_dict(self) -> t.Dict[str, t.Any]:
        """
        Convert the document into a json
        """
        doc = self.to_mongo().to_dict()

        if 'password' in doc:
            del doc['password']

        if '_id' in doc:
            doc['id'] = str(doc.pop('_id'))

        return doc
