#!/usr/bin/env python3
from app import create_app
from os import getenv
from flask import jsonify, render_template
from flask.typing import ResponseReturnValue

app = create_app(getenv('APP_DEV', 'dev'))


# HTTP Error Handlers


#index routes
@app.route('/', methods=['GET'])
def home():
    """
    Home route
    """
    return render_template('home.html')


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
