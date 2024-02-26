from app import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    user_email = db.Column(db.String(128), nullable=False)

    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'place_id': self.place_id,
            'user_email': self.user_email,
            # Include other fields
        }
