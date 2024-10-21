#!/usr/bin/env python3
"""
Module for user forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    URLField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email
)
from flask_wtf.file import FileAllowed


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    profile_picture = FileField('Profile Picture (Images only)', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    about = TextAreaField('Bio')
    location = StringField('Location')
    website = URLField('Website')
    skills = StringField('Skills')
    resume = FileField('Resume (PDF only)', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    industry = StringField('Industry')
