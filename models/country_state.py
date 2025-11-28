"""Country State model."""
from datetime import datetime
from db import db


class CountryState(db.Model):
    """State/Region model within a country."""
    __tablename__ = 'country_states'

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    recipes = db.relationship('Recipe', backref='state', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('country_id', 'name', name='uq_country_state'),
    )

    def to_dict(self):
        """Serialize state to dictionary."""
        return {
            'id': self.id,
            'country_id': self.country_id,
            'name': self.name,
            'country': self.country.to_dict() if self.country else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<CountryState {self.name}>'

