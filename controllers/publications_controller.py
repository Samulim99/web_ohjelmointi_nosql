from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from models import Publication

@jwt_required(optional=True)
def publications_route_handler():
    logged_in_user = get_jwt()
    if request.method == 'GET':
        if logged_in_user:
            if logged_in_user['role'] == 'admin':
                publications = Publication.get_all()
            elif logged_in_user['role'] == 'user':
                publications = Publication.get_by_owner_and_visibility(user = logged_in_user, visibility=[1,2])

        else:
            return ""


        return jsonify(publications=Publication.list_to_json(publications))
    
    elif request.method == 'POST':
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url']
        new_publication = Publication(title, description, url)
        new_publication.create()
        return jsonify(publication = new_publication)