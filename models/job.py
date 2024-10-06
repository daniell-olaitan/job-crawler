#!/usr/bin/env python3
"""
Module for job related models
"""
from models.parent_model import ParentModel
from models.user import User
from typing import List
from datetime import datetime
from mongoengine import (
    Document,
    StringField,
    ListField,
    URLField,
    ReferenceField,
    DateTimeField
)


class JobListing(ParentModel, Document):
    title = StringField(required=True, max_length=255)
    description = StringField()
    application_url = URLField(required=True)
    skills_required = ListField(StringField(), required=True)
    location = StringField(required=True)
    salary = StringField()
    company_id = StringField(required=True)
    source = StringField(required=True, max_length=50)

    meta = {
        'collection': 'job_listings',
        'indexes': [
            'company_id',  # Index for querying job listings by company
        ]
    }

    def match_candidate(self, user_skills: List[str]) -> bool:
        return any(skill in user_skills for skill in self.skills_required)



class JobApplication(ParentModel, Document):
    user = ReferenceField(User, required=True)
    job = ReferenceField(JobListing, required=True)
    status = StringField(
        required=True,
        choices=["Applied", "Interview Scheduled", "Offer Received", "Rejected"],
        default="Applied"
    )
    applied_at = DateTimeField(default=datetime.now)
    notes = StringField()

    meta = {
        'collection': 'job_applications'
    }


class JobScraper(Document):
    source_url = StringField(required=True)

    meta = {
        'collection': 'job_scrapers'
    }
