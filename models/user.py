#!/usr/bin/env python3
"""
Module for user model
"""
import os
from utils import delete_file
from models import db
from typing import List
from flask_login import UserMixin
from mongoengine import (
    Document,
    StringField,
    URLField,
    signals
)
from app import app_bcrypt
from models.parent_model import ParentModel


class User(UserMixin, ParentModel, Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True, choices=['Job Seeker', 'Admin', 'Company', 'Super Admin'])
    location = StringField()
    profile_picture = StringField()
    about = StringField()
    status = StringField(required=True, default='active', choices=['active', 'inactive'])
    website = URLField()

    meta = {
        'collection': 'users',
        'ordering': ['-created_at']
    }

    def save_job(self, job: Document) -> None:
        user_profile = self.get_profile()
        db.add_relationship(user_profile, 'saved_jobs', job)

    def unsave_job(self, job: Document) -> None:
        user_profile = self.get_profile()
        db.remove_relationship(user_profile, 'saved_jobs', job)

    def get_company(self) -> Document:
        """
        Get the company if the user registers for company
        """
        from models.company import Company
        return db.find(Company, user=self)

    def get_profile(self) -> Document:
        from models.profile import Profile
        return db.find(Profile, user=self)

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


# Delete the profile picture when the user is deleted
def delete_profile_picture(sender, document, **kwargs):
    delete_file(document, os.getenv('IMAGE_UPLOAD_FOLDER'), 'profile_picture')

# Connect the function to the 'pre_delete' signal
signals.pre_delete.connect(delete_profile_picture, sender=User)
