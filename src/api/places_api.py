from flask import Blueprint, request, jsonify
from app import db
from models.places import Place

places_api = Blueprint('places_api', __name__)

@places_api.route('/places', methods=['GET'])
def get_saved_places():
    places = Place.query.all()
    return jsonify([place.to_dict() for place in places]), 200

@places_api.route('/places', methods=['POST'])
def save_place():
    data = request.json
    new_place = Place(name=data['name'], address=data['address'])
    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201

@places_api.route('/places/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'message': 'Place not found'}), 404
    
    data = request.json
    place.name = data.get('name', place.name)
    place.address = data.get('address', place.address)
    db.session.commit()
    return jsonify(place.to_dict()), 200

@places_api.route('/places/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'message': 'Place not found'}), 404
    
    db.session.delete(place)
    db.session.commit()
    return jsonify({'message': 'Place deleted successfully'}), 200
