"""Country model."""
from datetime import datetime
from db import db


class Country(db.Model):
    """Country model."""
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    code = db.Column(db.String(2), unique=True, index=True)
    continent = db.Column(db.String(50))
    lat = db.Column(db.Numeric(10, 8))
    lng = db.Column(db.Numeric(11, 8))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    states = db.relationship('CountryState', backref='country', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """Serialize country to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'continent': self.continent,
            'lat': float(self.lat) if self.lat else None,
            'lng': float(self.lng) if self.lng else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Country {self.name}>'

