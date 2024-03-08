from flask import Blueprint, request, jsonify
import requests
import os

# Initialise Blueprint
places_bp = Blueprint("places", __name__)

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PLACES_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_API_URL = "https://maps.googleapis.com/maps/api/place/details/json"


# Get place details by place_id and location
@places_bp.route("/lookup_places", methods=["GET"])
def lookup_places():
    input_text = request.args.get("input")
    location = request.args.get("location")
    if not input_text:
        return jsonify({"error": "Missing input parameter"}), 400

    params = {
        "query": input_text,
        "location": location,
        "radius": "15000",
        "key": GOOGLE_API_KEY,
    }

    place_search_response = requests.get(PLACES_API_URL, params=params)
    if place_search_response.status_code == 200:
        places = place_search_response.json().get("results", [])

        for place in places:
            place_id = place.get("place_id")

            detail_params = {
                "place_id": place_id,
                "fields": "name,formatted_address,opening_hours,website,formatted_phone_number,wheelchair_accessible_entrance",
                "key": GOOGLE_API_KEY,
            }
            detail_response = requests.get(DETAILS_API_URL, params=detail_params)
            if detail_response.status_code == 200:
                place["details"] = detail_response.json().get("result", {})

            if "photos" in place and place["photos"]:
                photo_reference = place["photos"][0]["photo_reference"]
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
                place["photo_url"] = photo_url

        response = jsonify(places)
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response, place_search_response.status_code
    else:
        return (
            jsonify({"error": "Failed to fetch places"}),
            place_search_response.status_code,
        )
