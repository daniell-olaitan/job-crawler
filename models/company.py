#!/usr/bin/env python3
"""
Module for company model
"""
from models import db
from models.user import User
from models.parent_model import ParentModel
from mongoengine import (
    Document,
    StringField,
    ReferenceField,
    CASCADE
)


class Company(ParentModel, Document):
    industry = StringField( max_length=100)
    user = ReferenceField(
        User,
        index=True,
        required=True,
        reverse_delete_rule=CASCADE
    )

    meta = {
        'collection': 'companies'
    }

    def get_jobs(self):
        """
        Get the jobs posted by the company
        """
        from models.job_listing import JobListing
        return db.filter(JobListing, company=self)
