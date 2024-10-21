#!/usr/bin/env python3
"""
Module for job forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    FileField
)
from wtforms.validators import (
    DataRequired,
    Length
)
from flask_wtf.file import FileAllowed

class PostJobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Job Description')
    skills = StringField('Skills', validators=[DataRequired()])
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
    resume = FileField('Resume (PDF only)', validators=[FileAllowed(['pdf'], 'PDFs only!')])
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired()])
