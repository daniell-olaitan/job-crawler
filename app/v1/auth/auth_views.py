#!/usr/bin/python3
from models import db
from datetime import datetime
from app.v1.auth import auth
from models.user import (
    UserCreateValidator,
    UserLoginValidator
)
from models.invalid_token import InvalidToken
from flask.typing import ResponseReturnValue
from app.v1.auth.auth import Auth
from flask import (
    request,
    jsonify,
    session
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    jwt_required,
    decode_token
)

user_auth = Auth()


@auth.route('/register', methods=['POST'])
def register_user() -> ResponseReturnValue:
    """
    Register a new user
    """
    try:
        user_details = request.get_json()
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'data format required is json'
            }
        }), 400

    try:
        user_details = UserCreateValidator(**user_details)
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'provide valid and complete input'
            }
        }), 422

    try:
        user = user_auth.register_user(**user_details.model_dump())
        return jsonify({
            'status': 'success',
            'data': user.to_dict()
        }), 201
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {'error': str(err)}
        }), 400


@auth.route('/login', methods=['POST'])
def login() -> ResponseReturnValue:
    """
    Log in a user
    """
    try:
        login_details = request.get_json()
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'data format required is json'
            }
        }), 400

    try:
        login_details = UserLoginValidator(**login_details)
    except Exception as err:
        return jsonify({
            'status': 'fail',
            'data': {
                'error': 'provide valid and complete input'
            }
        }), 422

    try:
        user = user_auth.authenticate_user(**login_details.model_dump())
    except ValueError as err:
        return jsonify({
            'status': 'fail',
            'data': {'error': str(err)}
        }), 401

    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'status': 'success',
            'data': {
                'user': user.to_dict(),
                'access_token': access_token
            }
        }), 200

    return jsonify({
        'status': 'fail',
        'data': {'error': 'password is incorrect'}
    }), 401


@auth.route('/logout')
@jwt_required()
def logout() -> ResponseReturnValue:
    """
    Log out user
    """
    jti = get_jwt()['jti']
    db.insert(InvalidToken, jti=jti)

    return jsonify({
        'status': 'success',
        'data': {}
    }), 200
