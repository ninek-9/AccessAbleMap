import unittest
from unittest.mock import patch
from flask import Flask, json
from app.api import places


class TestPlacesBlueprint(unittest.TestCase):

    # Test set up
    def setUp(self):
        """Set up a Flask app for testing."""
        app = Flask(__name__)
        app.register_blueprint(places.places_bp)
        app.config["TESTING"] = True
        self.client = app.test_client()

    # Test looking up places is successful
    @patch("requests.get")
    def test_lookup_places_success(self, mock_get):
        """Test the /lookup_places endpoint for successful API call."""
        # Mocking the requests.get response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4",
                    "name": "Google",
                    "details": {
                        "formatted_address": "Mountain View, CA",
                        "opening_hours": {},
                        "website": "https://www.google.com",
                        "formatted_phone_number": "1234567890",
                        "wheelchair_accessible_entrance": "yes",
                    },
                }
            ]
        }

        # Making a GET request to the endpoint
        response = self.client.get("/lookup_places?input=Google&location=MountainView")
        data = json.loads(response.data)

        # Assertions to validate the endpoint behavior
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(data[0]["name"], "Google")

    # Test looking up places fails
    @patch("requests.get")
    def test_lookup_places_failure(self, mock_get):
        """Test the /lookup_places endpoint for failed API call."""
        # Mocking the requests.get response to simulate an API failure
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        # Making a GET request to the endpoint
        response = self.client.get("/lookup_places?input=Google&location=MountainView")

        # Assertions to validate the endpoint behavior
        self.assertEqual(response.status_code, 500)
        self.assertIn("error", json.loads(response.data))


if __name__ == "__main__":
    unittest.main()
