"""
Related groups of API endpoints are implemented as Flask Blueprints

Blueprints take advantage of OO inheritance to derive new versions from old,
and app mountpoints (url_prefix) to support multiple versions simultaneously

Flask "views" should only be concerned about unpacking requests, delegating
all business logic to a library function, and formatting the library output
into a response
"""
from logging import getLogger

from flask import Blueprint, jsonify, make_response, request

log = getLogger(__name__)

FlaskAPIv1 = Blueprint('v1', __name__, url_prefix='/v1')

@FlaskAPIv1.route('/hello', methods=['GET', 'POST'])
def hello():
    name = request.args.get("name") or "World"
    response = make_response(f"Hello {name}!")
    response.mimetype = "text/plain"
    return response

