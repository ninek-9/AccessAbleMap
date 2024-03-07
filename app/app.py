'''from flask import Blueprint, request, jsonify, current_app
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Blueprint
places_bp = Blueprint('places', __name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

@places_bp.route('/lookup_places', methods=['GET'])
def lookup_places():
    input_text = request.args.get('input')
    location = request.args.get('location')
    if not input_text:
        return jsonify({'error': 'Missing input parameter'}), 400

    # url = PLACES_API_URL + '?query=' + input_text + '&location=' + location + '&radius=15000' + '&key=' + GOOGLE_MAPS_API_KEY
    params = {
        'query': input_text,
        #'inputtype': 'textquery',
        #'fields': 'name,formatted_address,geometry,place_id',
        'location': location,
        'radius': '15000',
        'key': GOOGLE_MAPS_API_KEY
    }
    # print(url)
    response = requests.get(PLACES_API_URL, params=params)
    # response = requests.get(url)
    # print(response.status_code)

    if response.status_code == 200:
        return response.json()
    else:
        return jsonify({'error': 'Failed to fetch places'}), response.status_code


@places_bp('/place_details', methods=['GET'])
def get_place_details():
    place_id = request.args.get('place_id')
    if not place_id:
        return jsonify({'error': 'Missing place_id parameter'}), 400

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,address_component,formatted_address,photo,review,website,formatted_phone_number',
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(details_url, params=params)
    if response.status_code == 200:
        return jsonify(response.json()['result'])
    else:
        return jsonify({'error': 'Failed to fetch place details'}), response.status_code
'''



'''from flask import Flask
from api.places import places_bp
from api.reviews import reviews_bp

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')  # or ProductionConfig
 
app.register_blueprint(places_bp, url_prefix='/api')
app.register_blueprint(reviews_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
    app.run(debug=True)'''


'''from dotenv import load_dotenv
from flask import Flask, jsonify, request
import os
import requests
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Function to get database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

# Lookup places using Google Places API
@app.route('/lookup_places', methods=['GET'])
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

# Get detailed information of a place
@app.route('/place_details', methods=['GET'])
def get_place_details():
    place_id = request.args.get('place_id')
    if not place_id:
        return jsonify({'error': 'Missing place_id parameter'}), 400

    params = {
        'place_id': place_id,
        'fields': 'name,address_component,formatted_address,photos,reviews,website,formatted_phone_number',
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(DETAILS_API_URL, params=params)
    if response.status_code == 200:
        return jsonify(response.json()['result'])
    else:
        return jsonify({'error': 'Failed to fetch place details'}), response.status_code

# Fetch reviews from the database
@app.route('/reviews/<place_id>', methods=['GET'])
def get_reviews(place_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM reviews WHERE place_id = %s', (place_id,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reviews)

# Post a review to the database
@app.route('/reviews', methods=['POST'])
def post_review():
    review_data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO reviews (user_email, place_id, review, rating) VALUES (%s, %s, %s, %s)',
                   (review_data['user_email'], review_data['place_id'], review_data['review'], review_data['rating']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    app.run(debug=True)'''

'''
from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from src.config.config import Config
from dotenv import load_dotenv
import os
import requests
import psycopg2

load_dotenv()  # Load variables from .env file

app = Flask(__name__)

GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')  # Make sure to set this in your environment variables
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

# Lookup places using Google Places API
@app.route('/lookup_places', methods=['GET'])
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


@app.route('/place_details', methods=['GET'])
def get_place_details():
    place_id = request.args.get('place_id')
    if not place_id:
        return jsonify({'error': 'Missing place_id parameter'}), 400

    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'fields': 'name,address_component,formatted_address,photo,review,website,formatted_phone_number',
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(details_url, params=params)
    if response.status_code == 200:
        return jsonify(response.json()['result'])
    else:
        return jsonify({'error': 'Failed to fetch place details'}), response.status_code


# Get database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn


# Get saved places from database
def get_saved_places(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM places WHERE user_id = %s', (user_id,))
    places = cur.fetchall()
    cur.close()
    conn.close()
    return places

# Return saved places to user
@app.route('/saved_places', methods=['GET'])
def saved_places():
    user_id = request.args.get('user_id')  # Assuming user_id is passed as a query parameter
    places = get_saved_places(user_id)
    return jsonify(places)

if __name__ == '__main__':
    app.run(debug=True)



add post and get reviews with place id
add review to database: user, place id, review, rating
get user reviews + get place reviews
ask chatgpt to write reviews in query form
places: return latitude and longitude for all pins and place ID to get info.
place info: name, addreess, picture{s), reviews, link to website, phone number, email, etc. maybe link to google maps


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

if __name__ == '__main__':
    db.create_all()  # Creates database tables
    app.run(debug=True)
    

load_dotenv()  # Load variables from .env file
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
app = Flask(__name__)

app.register_blueprint(place_api, url_prefix='/api')
app.config.from_object(Config)
db = SQLAlchemy(app)

# Example endpoint
@app.route('/api/places', methods=['GET'])
def get_places():
    # Logic to fetch and return places
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places])

if __name__ == '__main__':
    from src.app import db
    with app.app_context():
        db.create_all()
    app.run(debug=True)
'''