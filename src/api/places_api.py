from flask import Blueprint, jsonify

place_api = Blueprint('place_api', __name__)

@place_api.route('/places', methods=['GET'])
def get_places():
    # Dummy data - replace this with real database calls
    places = [
        {"id": 1, "name": "Place One"},
        {"id": 2, "name": "Place Two"}
    ]
    return jsonify(places)
