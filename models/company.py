#!/usr/bin/env python3
"""
Module for company model
"""
from models.parent_model import ParentModel
from models.job import JobListing
from mongoengine.fields import URLField
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField
)


class Company(ParentModel, Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    location = StringField()
    website = URLField()
    industry = StringField(max_length=100)
    jobs = ListField(ReferenceField(JobListing))

    meta = {
        'collection': 'companies'
    }
