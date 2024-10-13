#!/usr/bin/env python3
from app import create_app
from os import getenv
from models import db
from flask import jsonify, render_template
from flask.typing import ResponseReturnValue

app = create_app(getenv('APP_DEV', 'dev'))


# HTTP Error Handlers
@app.errorhandler(404)
def not_found(err: Exception) -> ResponseReturnValue:
    return render_template('errors/error_404.html')


#index routes
@app.route('/', methods=['GET'])
def home():
    """
    Home route
    """
    from models.job_listing import JobListing
    jobs = db.find_all(JobListing)

    return render_template('home.html', jobs=jobs)


@app.route('/privacy', methods=['GET'])
def privacy():
    """
    Display the privacy policy of Job Crawler
    """
    return render_template('privacy.html')


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
