import os
import requests

def lookup_place(place_name):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')  # Changed to fetch from environment
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": place_name,
        "inputtype": "textquery",
        "fields": "formatted_address,name,rating,opening_hours,geometry",
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None