#!/usr/bin/env python3
"""
Module for job application model
"""
import os
from utils import delete_file
from models.profile import Profile
from models.job_listing import JobListing
from models.parent_model import ParentModel
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    signals,
    CASCADE
)

class JobApplication(ParentModel, Document):
    user = ReferenceField(Profile, required=True, reverse_delete_rule=CASCADE)
    job = ReferenceField(JobListing, required=True, reverse_delete_rule=CASCADE)
    cover_letter = StringField()
    resume = StringField()
    status = StringField(
        required=True,
        choices=['submitted', 'under_review', 'interview_scheduled', 'rejected', 'offer_received'],
        default='submitted'
    )

    meta = {
        'collection': 'job_applications'
    }


# Delete the resume file when the user is deleted
def delete_resume_file(sender, document, **kwargs):
    delete_file(document, os.getenv('RESUME_UPLOAD_FOLDER'), 'resume')


# Connect the function to the 'pre_delete' signal
signals.pre_delete.connect(delete_resume_file, sender=JobApplication)
