#!/usr/bin/python3
from app.auth import auth
from models import db
from models.company import Company
from models.user import User
from flask.typing import ResponseReturnValue
from app.auth.auth_forms import (
    LoginForm,
    EmployerRegistrationForm,
    JobSeekerRegistrationForm,
    ForgotPasswordForm,
    ResetPasswordForm
)
from app.auth.auth import Auth
from flask import (
    request,
    render_template,
    redirect,
    flash,
    url_for
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

user_auth = Auth()


@auth.route('/register-job-seeker', methods=['GET', 'POST'])
def register_job_seeker() -> ResponseReturnValue:
    """
    Register a new job seeker user
    """
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = JobSeekerRegistrationForm()
    if form.validate_on_submit():
        user_details = request.form.to_dict()
        del user_details['csrf_token']
        del user_details['confirm_password']
        user_details.update(role='Job Seeker')
        try:
            user_auth.register_user(**user_details)
            flash('Registration successful, Please proceed to log in', 'success')

            return redirect(url_for('auth.login'))
        except ValueError as err:
            flash(str(err), 'error')
    return render_template('auth/register_job_seeker.html', form=form)


@auth.route('/register-employer', methods=['GET', 'POST'])
def register_employer() -> ResponseReturnValue:
    """
    Register a new employer user
    """
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = EmployerRegistrationForm()
    if form.validate_on_submit():
        user_details = request.form.to_dict()
        del user_details['csrf_token']
        del user_details['confirm_password']
        user_details.update(role='Employer')

        company_name = user_details.pop('company_name')
        company = db.insert(Company, name=company_name)

        user_details.update(company=company)
        try:
            user_auth.register_user(**user_details)
            flash('Registration successful, please proceed to log in', 'success')

            return redirect(url_for('auth.login'))
        except ValueError as err:
            flash(str(err), 'error')
    return render_template('auth/register_job_seeker.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login() -> ResponseReturnValue:
    """
    Log in a user
    """
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        login_details = request.form.to_dict()
        del login_details['csrf_token']
        try:
            user = user_auth.authenticate_user(**login_details)
            if user:
                login_user(user, remember=form.remember_me.data)
                flash('You are signed in', 'success')
                return redirect(url_for('home'))

            flash('Incorrect password', 'error')
        except ValueError as err:
            flash(str(err), 'error')
    return render_template('auth/login.html', form=form)


@auth.route('forgot-password', methods=['GET', 'POST'])
def forgot_password() -> ResponseReturnValue:
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = request.form['email']
        user = db.find(User, email=email)
        if user:
            try:
                user_auth.send_reset_link(user)
                flash('An email has been sent to your email address', 'info')
                return redirect(url_for('auth.login'))
            except Exception as err:
                flash(str(err), 'error')
        else:
            flash('Email is not registerd', 'error')
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/reset-password/<string:token>', methods=['GET', 'POST'])
def reset_password(token: str) -> ResponseReturnValue:
    if current_user.is_authenticated:
        flash('You are already logged in', 'success')
        return redirect(url_for('home'))
    user_id = user_auth.verify_reset_token(token)
    if not user_id:
        flash('The reset link is invalid or has expired.', 'warning')
        return redirect(url_for('auth.forgot_password'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = db.find(User, id=user_id)
        if user:
            db.update(User, id=user.id, password=form.new_password.data)
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form, token=token)


@auth.route('/logout')
@login_required
def logout() -> ResponseReturnValue:
    """
    Log out user
    """
    logout_user()
    flash('You are logged out', 'warning')
    return redirect(url_for('home'))
