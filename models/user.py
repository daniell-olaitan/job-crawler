#!/usr/bin/env python3
"""
Module for user model
"""
from flask_login import UserMixin
from typing import List
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
)
from app import app_bcrypt
# from models.company import Company
from models.parent_model import ParentModel


class User(UserMixin, ParentModel, Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, choices=["Job Seeker", "Employer"])
    skills = ListField(StringField(), default=[])  # Only for Job Seekers
    profile_picture = StringField()  # URL to profile picture
    resume = StringField()  # URL to resume
    company = ReferenceField('Company')

    meta = {
        'collection': 'users',
        'indexes': [{'fields': ['email', 'id'], 'unique': True}],
        'ordering': ['-created_at']
    }

    def pre_save(self) -> None:
        self.password = app_bcrypt.generate_password_hash(self.password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return app_bcrypt.check_password_hash(self.password, password)

    def match_jobs(self, jobs: List[str]) -> List[str]:
        """Matches the user’s skills to job listings."""
        if self.role != 'Job Seeker':
            return []
        matched_jobs = [job for job in jobs if any(skill in job.skills_required for skill in self.skills)]
        return matched_jobs
