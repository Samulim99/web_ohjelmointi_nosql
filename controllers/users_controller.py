from flask import jsonify, request
from models import User, db
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required

@jwt_required()
def users_route_handler():
    if request.method == 'GET':
        users = User.get_all()
        
        return jsonify(users=User.list_to_json(users))

    elif request.method == 'POST':
        request_body = request.get_json()
        username = request_body['username']
        new_user = User(username)

        new_user.create()
        return jsonify(user=new_user.to_json())

        """ result = db.users.insert_one({'username' : request_body['username']})
        new_user = {
            '_id': str(result.inserted_id),
            'username': request_body['username']
        }
        return jsonify(user=new_user) """

def user_route_handler(_id):
    if request.method == 'GET':
        user = user.get_by_id(_id)
        return jsonify(user=user.to_json())
    elif request.method == 'DELETE':
        user = User.get_by_id(_id)
        user.delete()
        return ""
    elif request.method == 'PATCH':
        # 1 ota vastaan data clientiltä (puhelin appi / selain / insomnia rest client)
        request_body = request.get_json()
        new_username = request_body['username']
        """ user = User.get_by_id(_id)
        user.username = new_username
        user.update() """
        user = User.update_by_id(_id, new_username)

        return jsonify(user=user.to_json())