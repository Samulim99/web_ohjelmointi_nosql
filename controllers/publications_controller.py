from flask import jsonify, request

from models import Publication

def publications_route_handler():
    if request.method == 'GET':
        publications = Publication.get_all()
        return jsonify(publications=Publication.list_to_json(publications))
    
    elif request.method == 'POST':
        request_body = request.get_json()
        title = request_body['title']
        description = request_body['description']
        url = request_body['url']
        new_publication = Publication(title, description, url)
        new_publication.create()
        return jsonify(publication = new_publication)