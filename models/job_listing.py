#!/usr/bin/env python3
"""
Module for job listing model
"""
from models.parent_model import ParentModel
from models.company import Company
# from models.user import User
from typing import List
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
    IntField,
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
    applications_count = IntField(default=0)

    meta = {
        'collection': 'job_listings',
        'ordering': ['-created_at']
    }

    def match_candidate(self, user_skills: List[str]) -> bool:
        return any(skill in user_skills for skill in self.skills_required)
