#!/usr/bin/env python3
"""
Module for job views
"""
import os
import uuid
from models import db
from models.user import User
from werkzeug.utils import secure_filename
from app.job.job_forms import JobApplicationForm
from flask import (
    request,
    render_template,
    redirect,
    flash,
    url_for,
     abort,
     current_app
)
from flask_login import (
    login_required,
    current_user
)
from app.job.job_forms import (
    PostJobForm
)
from models.job_listing import JobListing
from models.job_application import JobApplication
from app.job import job_views
from flask.typing import ResponseReturnValue
from app.auth.auth import Auth

auth = Auth()


@job_views.route('/apply-for-job/<string:job_id>', methods=['GET', 'POST'])
@login_required
@auth.role_required('Job Seeker')
def apply_for_job(job_id: str) -> ResponseReturnValue:
    job = db.find(JobListing, id=job_id)
    if not job:
        abort(404)

    user_profile = current_user.get_profile()
    application = db.find(JobApplication, job=job, user=user_profile)
    if not application:
        form = JobApplicationForm()
        if form.validate_on_submit():
            resume = form.resume.data
            filename = secure_filename(resume.filename)
            filename = str(uuid.uuid4()) + filename
            resume.save(os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], filename))
            db.insert(
                JobApplication,
                user=current_user.get_profile(),
                job=job,
                cover_letter=form.cover_letter.data,
                resume=filename
            )

            db.update(JobListing, job.id, applications_count=job.applications_count+1)
            flash('Application submitted', 'success')
            return redirect(url_for('job_views.view_job_details', job_id=job_id))
        return render_template('job/job_application.html', form=form, job=job)

    return redirect(url_for('job_views.view_job_details', job_id=job_id))


@job_views.route('/update-job-application/<string:job_id>', methods=['GET', 'POST'])
@login_required
@auth.role_required('Job Seeker')
def update_job_application(job_id: str) -> ResponseReturnValue:
    job = db.find(JobListing, id=job_id)
    if not job:
        abort(404)

    user_profile = current_user.get_profile()
    application = db.find(JobApplication, job=job, user=user_profile)
    if application:
        form = JobApplicationForm(cover_letter=application.cover_letter)

        if form.validate_on_submit():
            resume = form.resume.data
            filename = secure_filename(resume.filename)
            filename = str(uuid.uuid4()) + filename
            file_path = os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], application.resume)
            if os.path.exists(file_path):
                os.remove(file_path)

            resume.save(os.path.join(current_app.config['RESUME_UPLOAD_FOLDER'], filename))
            db.update(
                JobApplication,
                id=application.id,
                cover_letter=form.cover_letter.data,
                resume=filename
            )

            flash('Application updated', 'info')
            return redirect(url_for('user_views.dashboard'))
        return render_template('job/job_application_update.html', form=form, job=job)

    return redirect(url_for('job_views.view_job_details', job_id=job_id))


@job_views.route('/cancel-job-application/<string:job_id>', methods=['GET'])
@login_required
@auth.role_required('Job Seeker')
def cancel_job_application(job_id: str) -> ResponseReturnValue:
    job = db.find(JobListing, id=job_id)
    user_profile = current_user.get_profile()
    if not (user_profile and job):
        abort(404)

    application = db.find(JobApplication, job=job, user=user_profile)
    if not application:
        abort(404)

    db.delete(
        JobApplication,
        application.id
    )

    db.update(JobListing, job.id, applications_count=job.applications_count-1)
    flash('Application cancelled', 'info')

    referer = request.headers.get("Referer")
    return redirect(referer or url_for('user_views.dashboard'))


@job_views.route('/view-job/<string:job_id>', methods=['GET'])
def view_job_details(job_id: str) -> ResponseReturnValue:
    applied = False
    job = db.find(JobListing, id=job_id)
    if not job:
        abort(404)

    if (current_user.is_authenticated and
        job.source == 'Company' and
            current_user.role == 'Job Seeker'):
        user_profile = current_user.get_profile()
        if user_profile:
            application = db.find(JobApplication, job=job, user=user_profile)

        if application:
            applied = True

    return render_template('job/job_details.html', job=job, applied=applied)


@job_views.route('/view-applications/<string:job_id>', methods=['GET', 'POST'])
@login_required
@auth.role_required('Company')
def view_applications(job_id: str) -> ResponseReturnValue:
    """
    View applications on a job
    """
    pass


@job_views.route('/save-job/<string:job_id>', methods=['GET'])
@login_required
@auth.role_required('Job Seeker')
def save_job(job_id: str) -> ResponseReturnValue:
    """
    Save a job
    """
    job = db.find(JobListing, id=job_id)
    if not job:
        abort(404)

    current_user.save_job(job)
    flash('Job saved', 'success')

    return redirect(url_for('job_views.view_job_details', job_id=job_id))


@job_views.route('/unsave-job/<string:job_id>', methods=['GET'])
@login_required
@auth.role_required('Job Seeker')
def unsave_job(job_id: str) -> ResponseReturnValue:
    """
    Unsave a job
    """
    job = db.find(JobListing, id=job_id)
    if not job:
        abort(404)

    current_user.unsave_job(job)
    flash('Job unsaved', 'info')

    return redirect(url_for('job_views.view_job_details', job_id=job_id))


@job_views.route('/view-saved-jobs', methods=['GET'])
@login_required
@auth.role_required('Job Seeker')
def view_saved_jobs() -> ResponseReturnValue:
    return render_template('job/saved_jobs.html')


@job_views.route('/delete-job/<string:job_id>')
@login_required
@auth.role_required('Company')
def delete_job(job_id: str) -> ResponseReturnValue:
    """
    Delete a job posting
    """
    db.delete(JobListing, id=job_id)
    flash('Job deleted', 'info')

    return redirect(url_for('user_views.dashboard'))


@job_views.route('/post-job', methods=['GET', 'POST'])
@login_required
@auth.role_required('Company')
def post_job() -> ResponseReturnValue:
    """
    Post a job
    """
    form = PostJobForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        skills = [skill.data for skill in form.skills]

        details = request.form.to_dict()
        job_details = {
            'source': 'Company',
            'company': current_user.get_company(),
            'skills': skills
        }

        for key, val in details.items():
            if key.startswith('skills-') or key == 'csrf_token':
                continue

            job_details[key] = val

        _ = db.insert(JobListing, **job_details)
        flash('Job posted', 'success')

        return redirect(url_for('user_views.dashboard'))

    return render_template('job/post_job.html', form=form)


@job_views.route('/edit-job/<string:job_id>', methods=['GET', 'POST'])
@login_required
@auth.role_required('Company')
def edit_job(job_id: str) -> ResponseReturnValue:
    """
    Edit a posted job
    """
    company = current_user.get_company()
    job = db.find(JobListing, id=job_id, company=company)
    if not job:
        abort(404)

    form = PostJobForm(
        title=job.title,
        description=job.description,
        skills=job.skills,
        job_type=job.job_type,
        location=job.location,
        salary=job.salary
    )

    if form.validate_on_submit():
        skills = [skill.data for skill in form.skills]

        details = request.form.to_dict()
        job_details = {
            'skills': skills
        }

        for key, val in details.items():
            if key.startswith('skills-') or key == 'csrf_token':
                continue

            job_details[key] = val

        db.update(
            JobListing,
            id=job.id,
            **job_details
        )

        flash('Job updated', 'info')
        return redirect(url_for('user_views.dashboard'))

    return render_template('job/edit_job.html', form=form, job=job)
