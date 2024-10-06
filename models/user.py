#!/usr/bin/env python3
"""
Module for user model
"""
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)
from typing import (
    List,
    Optional
)
from mongoengine import (
    Document,
    StringField,
    ListField,
    ReferenceField,
)
from datetime import datetime
from app import app_bcrypt
from models.parent_model import ParentModel


# Pydantic model for validating input data
class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(..., regex="^(Job Seeker|Employer)$")
    skills: Optional[List[str]] = []  # Only applicable to job seekers
    profile_picture: Optional[str] = None
    resume: Optional[str] = None
    company_id: Optional[int] = None  # Only applicable to employers

    class Config:
        extra = 'forbid'


# Partial update schema for updating user profiles
class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr]
    password: Optional[str] = Field(None, min_length=6)
    profile_picture: Optional[str]
    resume: Optional[str]
    skills: Optional[List[str]] = []
    company_id: Optional[int]

    class Config:
        extra = 'forbid'


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    class Config:
        extra = 'forbid'


class User(ParentModel, Document):
    name = StringField(required=True, max_length=100)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)  # Store hashed passwords
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
