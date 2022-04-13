
from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from errors.not_found import NotFound
from errors.validation_error import ValidationError
from models import User
from flask_jwt_extended import create_access_token


def register_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        #username = request_body.get('username, 'defaultvalue)
        password = request_body['password']
        new_user = User(username, password=password)
        new_user.create()
        return ""

def login_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        if request_body is None:
            raise ValidationError('Body is required')
        if 'username' not in request_body:
            raise ValidationError(message='Username is required')
        username = request_body['username']

        if 'password' not in request_body:
            raise ValidationError(message='Password is required')


        password = request_body['password']

        user = User.get_by_username(username)
        password_ok = sha256.verify(password, user.password)
        if password_ok:
            access_token = create_access_token(identity=str(user._id), additional_claims={'username': user.username, 'role': user.role})
            return jsonify(access_token=access_token)

        raise NotFound('User not found')
