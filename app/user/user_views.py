#!/usr/bin/env python3
"""
Module for user views
"""
from models import db
from flask import (
    request,
    render_template,
    redirect
)
from flask_login import (
    login_required,
    current_user
)
# from models.job_listing import JobListing
from models.job_application import JobApplication
from app.user import user_views
from flask.typing import ResponseReturnValue

@user_views.route('/dashboard')
@login_required
def dashboard() -> ResponseReturnValue:
    """
    Display the user dashboard
    """
    if current_user.role == 'Job Seeker':
        user_profile = current_user.get_profile()
        applications = db.filter(JobApplication, user=user_profile)
        return render_template('user/job_seeker_dashboard.html', applications=applications)
    elif current_user.role == 'Company':
        jobs = current_user.get_company().get_jobs()
        return render_template('user/company_dashboard.html', jobs=jobs)


@user_views.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass


@user_views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile() -> ResponseReturnValue:
    return render_template('user/profile.html')
