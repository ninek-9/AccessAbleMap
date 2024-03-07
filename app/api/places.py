from flask import Blueprint, request, jsonify
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Initialize Blueprint
places_bp = Blueprint('places', __name__)

# Load environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PHOTO_API_URL = "https://maps.googleapis.com/maps/api/place/photo"

# Function to get database connection
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

# Function to get reviews from the database
def get_reviews_for_place(place_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM reviews WHERE place_id = %s', (place_id,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return reviews

@places_bp.route('/lookup_places', methods=['GET'])
def lookup_places():
    input_text = request.args.get('input')
    location = request.args.get('location')
    if not input_text:
        return jsonify({'error': 'Missing input parameter'}), 400

    params = {
        'query': input_text,
        'location': location,
        'radius': '15000',
        'key': GOOGLE_API_KEY
    }

    place_search_response = requests.get(PLACES_API_URL, params=params)
    if place_search_response.status_code == 200:
        places = place_search_response.json().get('results', [])

        # Enrich each place with details and reviews
        for place in places:
            place_id = place.get('place_id')

            # Fetch place details
            detail_params = {
                'place_id': place_id,
                'fields': 'name,formatted_address,opening_hours,website,formatted_phone_number,wheelchair_accessible_entrance',
                'key': GOOGLE_API_KEY
            }
            detail_response = requests.get(DETAILS_API_URL, params=detail_params)
            if detail_response.status_code == 200:
                place['details'] = detail_response.json().get('result', {})
                
            # photo_params = {
            #     'photoreference': place['photos'][0]['photo_reference'],
            #     'key': GOOGLE_API_KEY
            # }
            # photo_response = requests.get(PHOTO_API_URL, params=photo_params)
            if 'photos' in place and place['photos']:
                photo_reference = place['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
                place['photo_url'] = photo_url

            # Fetch reviews from the database
            place['reviews'] = get_reviews_for_place(place_id)

        response = jsonify(places)
        response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:5000')

        return response, place_search_response.status_code
    else:
        return jsonify({'error': 'Failed to fetch places'}), place_search_response.status_code
    
# make place detail for all of them and add to the same route + link reviews to places details
# deploy to azure
# link reviews to users POST request + email, reviews, rating