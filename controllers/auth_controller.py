
from os import access
from flask import jsonify, request
from passlib.hash import pbkdf2_sha256 as sha256
from errors.not_found import NotFound
from errors.validation_error import ValidationError
from models import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, jwt_required
from flask.views import MethodView
from validators.account import validate_account

from validators.validate_password_and_username import validate_password_and_username


def register_route_handler():
    if request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        #username = request_body.get('username, 'defaultvalue)
        password = request_body['password']
        new_user = User(username, password=password)
        new_user.create()
        return ""

@jwt_required()
#@validate_account
def account_route_handler():
    if request.method == 'GET':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        return jsonify(account=account.to_json())

    elif request.method == 'PATCH':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        request_body = request.get_json()
        if request_body:
            if 'username' in request_body:
                username = request_body['username']
                account.username = username
                account.update()
                return jsonify(account=account.to_json())
            raise ValidationError(message='username is required')
        raise ValidationError(message='request body is required')

@jwt_required()
def update_password_route_handler():
    if request.method == 'PATCH':
        logged_in_user = get_jwt()
        account = User.get_by_id(logged_in_user['sub'])
        request_body = request.get_json()
        if request_body:
            if 'password' in request_body:
                password = request_body['password']
                account.password = sha256.hash(password)
                account.update()
                return jsonify(account=account.to_json())
            raise ValidationError(message='password is required')
        raise ValidationError(message='request body is required')


class LoginRouteHandler(MethodView):
    @validate_password_and_username
    def post(self):

        request_body = request.get_json()
        username = request_body['username']

        password = request_body['password']

        user = User.get_by_username(username)

        password_ok = sha256.verify(password, user.password)
        if password_ok:
            access_token = create_access_token(identity=str(user._id), additional_claims={'username': user.username, 'role': user.role})
            refresh_token = create_refresh_token(identity=str(user._id))
            return jsonify(access_token=access_token, refresh=refresh_token)

        raise NotFound('User not found')


    @jwt_required(refresh=True)
    def patch(self):
        logged_in_user = get_jwt()
        user = User.get_by_id(logged_in_user['sub'])
        access_token = create_access_token(identity=str(user._id), additional_claims={'username': user.username, 'role': user.role})
        return jsonify(access=access_token)



