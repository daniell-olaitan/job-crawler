#!/usr/bin/env python3
from app import create_app
from os import getenv
from models import db
from flask import (
    jsonify,
    render_template,
    request
)
from flask.typing import ResponseReturnValue

app = create_app(getenv('APP_DEV', 'dev'))
from models.user import User

admin = db.find(User, name=getenv('admin_name'), email=getenv('admin_email'))
if not admin:
    db.insert(
        User,
        name=getenv('admin_name'),
        email=getenv('admin_email'),
        password=getenv('admin_pwd'),
        role='Super Admin'
    )


# HTTP Error Handlers
@app.errorhandler(401)
def unauthorozed(err: Exception) -> ResponseReturnValue:
    return render_template('errors/error_401.html')


@app.errorhandler(403)
def not_permited(err: Exception) -> ResponseReturnValue:
    return render_template('errors/error_403.html')


@app.errorhandler(404)
def not_found(err: Exception) -> ResponseReturnValue:
    return render_template('errors/error_404.html')


#index routes
@app.route('/', methods=['GET'])
def home() -> ResponseReturnValue:
    """
    Home route
    """
    from models.job_listing import JobListing

    jobs = db.find_all(JobListing)
    return render_template('home.html', jobs=jobs)


@app.route('/search', methods=['GET'])
def search() -> ResponseReturnValue:
    from models.job_listing import JobListing

    search_query = request.args.get('q')
    if search_query:
        jobs = JobListing.objects.search_text(search_query)
        return render_template('job/search_results.html', jobs=jobs, search_query=search_query)

    jobs = db.find_all(JobListing)
    return render_template('home.html', jobs=jobs)


@app.route('/privacy', methods=['GET'])
def privacy() -> ResponseReturnValue:
    """
    Display the privacy policy of Job Crawler
    """
    return render_template('privacy.html')


@app.route('/terms-of-service', methods=['GET'])
def terms_of_service() -> ResponseReturnValue:
    """
    Display the terms of service of Job Crawler
    """
    return render_template('terms_of_service.html')


@app.route('/status', methods=['GET'])
def app_status() -> ResponseReturnValue:
    """
    Get the status of the application
    """
    return jsonify({
        'status': 'success',
        'data': {
            'app_status': 'active'
        }
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
