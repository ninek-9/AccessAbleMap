from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask_cors import CORS

# Initialize Blueprint
reviews_bp = Blueprint('reviews', __name__)
CORS(reviews_bp, origins=['http://127.0.0.1:5000']) 

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn

@reviews_bp.route('/reviews/place_id', methods=['GET'])
def get_place_reviews():
    place_id = request.args.get('place_id')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM reviews WHERE place_id = %s', (place_id,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reviews)

@reviews_bp.route('/reviews/user', methods=['GET'])
def get_user_reviews():
    user_email = request.args.get('user_email')
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM reviews WHERE user_email = %s', (user_email,))
    reviews = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reviews)

@reviews_bp.route('/reviews', methods=['POST'])
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
