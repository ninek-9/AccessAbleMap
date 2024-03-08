import unittest
import pytest
from unittest.mock import patch, MagicMock
from app import create_app


# Creating a fixture to set up a Flask app for testing
@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# Testing database connection for reviews by places
@patch("app.api.reviews.get_db_connection")
def test_get_place_reviews(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {
            "id": 24,
            "place_id": "ChIJAQoi2mcFdkgRhi5pHDcbkTE",
            "rating": "5",
            "review": "Accessible campus",
            "user_email": "user@example.com",
            "place_name": "Imperial",
        }
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    response = client.get("/api/reviews/place_id?place_id=ChIJAQoi2mcFdkgRhi5pHDcbkTE")
    assert response.status_code == 200
    assert response.json == [
        {
            "id": 24,
            "place_id": "ChIJAQoi2mcFdkgRhi5pHDcbkTE",
            "rating": "5",
            "review": "Accessible campus",
            "user_email": "user@example.com",
            "place_name": "Imperial",
        }
    ]


# Testing database connection for reviews by users
@patch("app.api.reviews.get_db_connection")
def test_get_user_reviews(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        {
            "id": 24,
            "place_id": "ChIJAQoi2mcFdkgRhi5pHDcbkTE",
            "rating": "5",
            "review": "Accessible campus",
            "user_email": "user@example.com",
            "place_name": "Imperial",
        }
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    response = client.get("/api/reviews/user?user_email=user@example.com")
    assert response.status_code == 200
    assert response.json == [
        {
            "id": 24,
            "place_id": "ChIJAQoi2mcFdkgRhi5pHDcbkTE",
            "rating": "5",
            "review": "Accessible campus",
            "user_email": "user@example.com",
            "place_name": "Imperial",
        }
    ]


# Testing database connection for posting a review
@patch("app.api.reviews.get_db_connection")
def test_post_review(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_db_connection.return_value = mock_conn

    response = client.post(
        "/api/reviews",
        json={
            "user_email": "user@example.com",
            "place_id": "ChIJAQoi2mcFdkgRhi5pHDcbkTE",
            "review": "Great place",
            "rating": "5",
            "place_name": "Imperial",
        },
    )

    assert response.status_code == 201
    assert response.json == {"status": "success"}
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
