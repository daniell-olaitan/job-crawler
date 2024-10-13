#!/usr/bin/env python3
"""
Module for user profile model
"""
from models.user import User
from models.job_listing import JobListing
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    PULL,
    CASCADE
)
from models.parent_model import ParentModel


class Profile(ParentModel, Document):
    skills = ListField(StringField(), default=[])
    resume = StringField()
    saved_jobs = ListField(ReferenceField(JobListing, reverse_delete_rule=PULL))
    user = ReferenceField(
        User,
        index=True,
        required=True,
        reverse_delete_rule=CASCADE
    )
