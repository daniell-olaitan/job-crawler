#!/usr/bin/env python3
"""
Module for job application model
"""
import os
from models.profile import Profile
from models.job_listing import JobListing
from models.parent_model import ParentModel
from typing import List
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    IntField,
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
        choices=["Applied", "Interview Scheduled", "Offer Received", "Rejected"],
        default="Applied"
    )

    meta = {
        'collection': 'job_applications'
    }


# Function to delete the resume file when a application is withdrawn is deleted
def delete_resume_file(sender, document, **kwargs):
    if document.resume:
        file_path = os.path.join(os.getenv('RESUME_UPLOAD_FOLDER'), document.resume)
        if os.path.exists(file_path):
            os.remove(file_path)


# Connect the function to the 'pre_delete' signal
signals.pre_delete.connect(delete_resume_file, sender=JobApplication)
