"""Favorite model."""
from datetime import datetime
from db import db


class Favorite(db.Model):
    """Favorite model (polymorphic - can favorite users, recipes, states, countries)."""
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    favorite_type = db.Column(db.String(20), nullable=False, index=True)  # 'user', 'recipe', 'state', 'country'
    favorite_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'favorite_type', 'favorite_id', name='uq_user_favorite'),
        db.CheckConstraint("favorite_type IN ('user', 'recipe', 'state', 'country')", name='check_favorite_type'),
    )

    def to_dict(self):
        """Serialize favorite to dictionary."""
        favorite_data = None
        if self.favorite_type == 'recipe':
            from .recipe import Recipe
            favorite_obj = Recipe.query.get(self.favorite_id)
            favorite_data = favorite_obj.to_dict(include_steps=False) if favorite_obj else None
        elif self.favorite_type == 'user':
            from .user import User
            favorite_obj = User.query.get(self.favorite_id)
            favorite_data = favorite_obj.to_public_dict() if favorite_obj else None
        elif self.favorite_type == 'state':
            from .country_state import CountryState
            favorite_obj = CountryState.query.get(self.favorite_id)
            favorite_data = favorite_obj.to_dict() if favorite_obj else None
        elif self.favorite_type == 'country':
            from .country import Country
            favorite_obj = Country.query.get(self.favorite_id)
            favorite_data = favorite_obj.to_dict() if favorite_obj else None

        return {
            'id': self.id,
            'user_id': self.user_id,
            'favorite_type': self.favorite_type,
            'favorite_id': self.favorite_id,
            'favorite_data': favorite_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<Favorite {self.favorite_type}:{self.favorite_id} by user {self.user_id}>'

