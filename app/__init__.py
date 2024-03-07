from flask import Flask
from app.api.places import places_bp
from app.api.reviews import reviews_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5000"}})
    app.config.from_object('app.config.config.ProductionConfig')

    app.register_blueprint(places_bp, url_prefix='/api')
    app.register_blueprint(reviews_bp, url_prefix='/api')

    return app
