#!/usr/bin/env python3
"""
Module for user views
"""
import os
import uuid
from models import db
from models.user import User
from models.company import Company
from models.profile import Profile
from models.job_listing import JobListing
from werkzeug.utils import secure_filename
from flask import (
    url_for,
    render_template,
    redirect,
    current_app,
    flash,
    request,
    abort
)
from flask_login import current_user
from models.user import User
from app.user.user_forms import EditProfileForm
from models.job_application import JobApplication
from app.user import user_views
from flask.typing import ResponseReturnValue
from app.auth.auth import Auth

auth = Auth()


@user_views.route('/dashboard', methods=['GET'])
@auth.login_required()
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
    elif current_user.role == 'Admin':
        total_job_seekers = len(db.filter(User, role='Job Seeker'))
        total_companies = len(db.filter(User, role='Company'))
        total_users = total_companies + total_job_seekers
        total_jobs = len(db.find_all(JobListing))
        return render_template(
            'user/admin_dashboard.html',
            total_job_seekers=total_job_seekers,
            total_users=total_users,
            total_jobs=total_jobs,
            total_companies=total_companies,
        )
    elif current_user.role == 'Super Admin':
        total_job_seekers = len(db.filter(User, role='Job Seeker'))
        total_companies = len(db.filter(User, role='Company'))
        total_users = len(db.find_all(User))
        total_jobs = len(db.find_all(JobListing))
        total_admins = len(db.filter(User, role='Admin')) + 1
        return render_template(
            'user/admin_dashboard.html',
            total_job_seekers=total_job_seekers,
            total_users=total_users,
            total_jobs=total_jobs,
            total_companies=total_companies,
            total_admins=total_admins
        )


@user_views.route('/edit-profile', methods=['GET', 'POST'])
@auth.login_required()
def edit_profile():
    user = db.find(User, id=current_user.id)
    form = EditProfileForm()
    if request.method == 'GET':
        if user.role == 'Job Seeker':
            skills = ', '.join(user.get_profile().skills)
            form = EditProfileForm(
                name=user.name,
                email=user.email,
                about=user.about,
                location=user.location,
                website=user.website,
                skills=skills
            )
        elif user.role == 'Company':
            industry = user.get_company().industry
            form = EditProfileForm(
                name=user.name,
                email=user.email,
                about=user.about,
                location=user.location,
                website=user.website,
                industry=industry
            )
        else:
            form = EditProfileForm(
                name=user.name,
                email=user.email,
                about=user.about,
                location=user.location,
                website=user.website,
            )

    if form.validate_on_submit():
        profile_details = {
            'name': form.name.data,
            'email': form.email.data,
            'about': form.about.data,
            'location': form.location.data,
            'website': form.website.data or None
        }

        profile_picture = form.profile_picture.data
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            filename = str(uuid.uuid4()) + filename
            if user.profile_picture:
                file_path = os.path.join(
                    current_app.config['IMAGE_UPLOAD_FOLDER'],
                    user.profile_picture
                )

                if os.path.exists(file_path):
                    os.remove(file_path)

            profile_picture.save(os.path.join(current_app.config['IMAGE_UPLOAD_FOLDER'], filename))
            profile_details.update(profile_picture=filename)

        db.update(
            User,
            id=user.id,
            **profile_details
        )

        if user.role == 'Job Seeker':
            skills = form.skills.data.split(', ')
            resume = form.resume.data
            if resume:
                filename = secure_filename(resume.filename)
                filename = str(uuid.uuid4()) + filename
                if user.get_profile().resume:
                    file_path = os.path.join(
                        current_app.config['RESUME_UPLOAD_FOLDER'],
                        user.get_profile().resume
                    )

                    if os.path.exists(file_path):
                        os.remove(file_path)

                resume.save(os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], filename))
                db.update(Profile, id=user.get_profile().id, resume=filename)

            if form.skills.data:
                db.update(Profile, id=user.get_profile().id, skills=skills)

        elif user.role == 'Company':
            if form.industry.data:
                db.update(Company, id=user.get_company().id, industry=form.industry.data)

        flash('Profile updated', 'info')
        return redirect(url_for('user_views.profile', user_id=current_user.id))

    return render_template('user/edit_profile.html', form=form)


@user_views.route('/delete-user/<string:user_id>', methods=['GET'])
@auth.login_required()
@auth.role_required('Super Admin', 'Admin')
def delete_user(user_id: str) -> ResponseReturnValue:
    user = db.find(User, id=user_id)
    if not user:
        abort(404)

    if current_user.role == 'Admin':
        if user.role in ['Admin', 'Super Admin']:
            abort(403)

    db.delete(User, user_id)
    flash('User deleted successfully', 'success')
    referer = request.headers.get("Referer")

    return redirect(referer or url_for('user_views.dashboard'))


@user_views.route('/suspend-user/<string:user_id>', methods=['GET'])
@auth.login_required()
@auth.role_required('Admin', 'Super Admin')
def suspend_user(user_id: str) -> ResponseReturnValue:
    user = db.find(User, id=user_id)
    if not user:
        abort(404)

    if current_user.role == 'Admin':
        if user.role in ['Admin', 'Super Admin']:
            abort(403)

    db.update(User, user_id, status='inactive')
    flash('User suspended successfully', 'success')
    referer = request.headers.get("Referer")

    return redirect(referer or url_for('user_views.dashboard'))


@user_views.route('/activate-user/<string:user_id>', methods=['GET'])
@auth.login_required()
@auth.role_required('Admin', 'Super Admin')
def activate_user(user_id: str) -> ResponseReturnValue:
    user = db.find(User, id=user_id)
    if not user:
        abort(404)

    if current_user.role == 'Admin':
        if user.role in ['Admin', 'Super Admin']:
            abort(403)

    db.update(User, user_id, status='active')
    flash('User activated successfully', 'success')
    referer = request.headers.get("Referer")

    return redirect(referer or url_for('user_views.dashboard'))


@user_views.route('/create-admin', methods=['GET', 'POST'])
@auth.login_required()
@auth.role_required('Super Admin')
def create_admin() -> ResponseReturnValue:
    from app.auth.auth_forms import JobSeekerRegistrationForm

    form = JobSeekerRegistrationForm()
    if form.validate_on_submit():
        user_details = request.form.to_dict()
        del user_details['csrf_token']
        del user_details['confirm_password']
        user_details.update(role='Admin')
        try:
            _ = auth.register_user(**user_details)
            flash('You have successfully created another admin', 'success')

            return redirect(url_for('user_views.dashboard'))
        except ValueError as err:
            flash(str(err), 'error')

    return render_template('user/register_admin.html', form=form)


@user_views.route('/manage-users', methods=['GET'])
@auth.login_required()
@auth.role_required('Admin', 'Super Admin')
def manage_users() -> ResponseReturnValue:
    from models.user import User
    from mongoengine import Q

    users = User.objects(Q(id__ne=current_user.id))
    if current_user.role == 'Admin':
        users = users.filter(Q(role='Job Seeker') | Q(role='Company'))

    return render_template('user/admin_user_management.html', users=users)


@user_views.route('/manage-jobs', methods=['GET'])
@auth.login_required()
@auth.role_required('Admin', 'Super Admin')
def manage_jobs() -> ResponseReturnValue:
    jobs = db.filter(JobListing)
    return render_template('user/admin_job_management.html', jobs=jobs)


@user_views.route('/profile/<string:user_id>', methods=['GET'])
@auth.login_required()
def profile(user_id: str) -> ResponseReturnValue:
    user = db.find(User, id=user_id)
    if not user:
        abort(404)

    if current_user.role not in ['Admin', 'Super Admin']:
        if user_id != current_user.id:
            abort(403)

    return render_template('user/profile.html', user=user)
