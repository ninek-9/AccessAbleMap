from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config

app = Flask(__name__)
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