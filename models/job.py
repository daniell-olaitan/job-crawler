#!/usr/bin/env python3
"""
Module for job model
"""
from models.parent_model import ParentModel
from mongoengine import (
    Document,
    URLField,
    StringField,
    ListField
)


class Job(ParentModel, Document):
    """
    Class to create job document in the collection
    """
    company_name = StringField(required=True, max_length=80)
    job_title = StringField(required=True, max_length=80)
    salary_range = StringField(max_length=60)
    application_url = URLField(required=True)
    job_description = ListField(StringField())
