#!/usr/bin/env python3
"""
Module for user profile model
"""
import os
from models.user import User
from utils import delete_file
from models.job_listing import JobListing
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    signals,
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


# Delete the resume file when the user is deleted
def delete_resume_file(sender, document, **kwargs):
    delete_file(document, os.getenv('RESUME_UPLOAD_FOLDER'), 'resume')


# Connect the function to the 'pre_delete' signal
signals.pre_delete.connect(delete_resume_file, sender=Profile)
