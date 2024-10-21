#!/usr/bin/env python3
"""
Module for job listing model
"""
from models import db
from models.parent_model import ParentModel
from models.company import Company
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    CASCADE
)


class JobListing(ParentModel, Document):
    title = StringField(required=True, max_length=255)
    description = StringField()
    skills = ListField(StringField(), required=True)
    location = StringField(required=True)
    salary = StringField()
    source = StringField(required=True, max_length=50)
    job_type = StringField(required=True)
    company = ReferenceField(Company, index=True, reverse_delete_rule=CASCADE)

    meta = {
        'collection': 'job_listings',
        'ordering': ['-updated_at'],
        'indexes': [
            {
                'fields': ['$title', '$description', '$skills', '$location', '$job_type'],
                'default_language': 'english'
            }
        ]
    }

    @property
    def application_count(self):
        from models.job_application import JobApplication

        applications = db.filter(JobApplication, job=self)
        return len(applications)
