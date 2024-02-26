from app import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256))


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            
        }
