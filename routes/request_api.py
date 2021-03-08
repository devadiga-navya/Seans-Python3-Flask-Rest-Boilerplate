"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from models import categories 
from validate_email import validate_email
from dbc import db
import json
from json import JSONEncoder

REQUEST_API = Blueprint('request_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

BOOK_REQUESTS = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        'title': u'Good Book',
        'email': u'testuser1@test.com',
        'timestamp': (datetime.today() - timedelta(1)).timestamp()
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        'title': u'Bad Book',
        'email': u'testuser2@test.com',
        'timestamp': (datetime.today() - timedelta(2)).timestamp()
    }
}


@REQUEST_API.route('/request', methods=['GET'])
def get_records():
    """Return all book requests
    @return: 200: an array of all known BOOK_REQUESTS as a \
    flask/response object with application/json mimetype.
    """ 
    result = []
    catList = categories.Categories.query.all()
    for data in catList :
        result.append({'id': data.id, 'name':data.name, 'description':data.description, 'parent category id':data.parent_id})
    return jsonify(result)

@REQUEST_API.route('/request/<string:_id>', methods=['GET'])
def get_record_by_id(_id):
    """Get book request details by it's id
    @param _id: the id
    @return: 200: a BOOK_REQUESTS as a flask/response object \
    with application/json mimetype.
    @raise 404: if book request not found
    """
    result = []
    catList = categories.Categories.query.filter_by(id = _id)
    for data in catList :
        result.append({'id': data.id, 'name':data.name, 'description':data.description, 'parent category id':data.parent_id})
    return jsonify(result)
 
@REQUEST_API.route('/request', methods=['POST'])
def create_record():
    """Create a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('title'):
        abort(400)

    new_uuid = str(uuid.uuid4())
    book_request = {
        'title': data['title'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }
    BOOK_REQUESTS[new_uuid] = book_request
    # HTTP 201 Created
    return jsonify({"id": new_uuid}), 201


@REQUEST_API.route('/request/<string:_id>', methods=['PUT'])
def edit_record(_id):
    """Edit a book request record
    @param email: post : the requesters email address
    @param title: post : the title of the book requested
    @return: 200: a booke_request as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    if _id not in BOOK_REQUESTS:
        abort(404)

    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)

    if not data.get('email'):
        abort(400)
    if not validate_email(data['email']):
        abort(400)
    if not data.get('title'):
        abort(400)

    book_request = {
        'title': data['title'],
        'email': data['email'],
        'timestamp': datetime.now().timestamp()
    }

    BOOK_REQUESTS[_id] = book_request
    return jsonify(BOOK_REQUESTS[_id]), 200


@REQUEST_API.route('/request/<string:_id>', methods=['DELETE'])
def delete_record(_id):
    """Delete a book request record
    @param id: the id
    @return: 204: an empty payload.
    @raise 404: if book request not found
    """
    catList = categories.Categories.query.filter_by(id = _id).delete()
    db.session.commit()
    return '', 204
