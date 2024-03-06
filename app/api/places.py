from flask import Blueprint, request, jsonify, current_app
import requests
import os

# Initialize Blueprint
places_bp = Blueprint('places', __name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

@places_bp.route('/lookup_places', methods=['GET'])
def lookup_places():
    input_text = request.args.get('input')
    if not input_text:
        return jsonify({'error': 'Missing input parameter'}), 400

    params = {
        'input': input_text,
        'inputtype': 'textquery',
        'fields': 'formatted_address,name,geometry,place_id',
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(PLACES_API_URL, params=params)
    if response.status_code == 200:
        return jsonify(response.json()['candidates'])
    else:
        return jsonify({'error': 'Failed to fetch places'}), response.status_code
