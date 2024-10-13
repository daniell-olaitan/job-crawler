#!/usr/bin/env python3
"""
Module for job forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    TextAreaField,
    SelectField,
    FieldList,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
)
from flask_wtf.file import FileAllowed

class PostJobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Job Description')
    skills = FieldList(StringField('Skills Required'), min_entries=1)
    location = StringField('Location', validators=[DataRequired()])
    salary = StringField('Salary')
    job_type = SelectField(
        'Job Type',
        choices=[
            ('Full-Time', 'Full-Time'),
            ('Part-Time', 'Part-Time'),
            ('Contract', 'Contract')
        ],
        validators=[DataRequired()]
    )


class JobApplicationForm(FlaskForm):
    resume = FileField('Resume (PDF only)', validators=[DataRequired(), FileAllowed(['pdf'], 'PDFs only!')])
    cover_letter = TextAreaField('Cover Letter')
