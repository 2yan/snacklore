"""Recipe Step model."""
from datetime import datetime
from db import db


class RecipeStep(db.Model):
    """Recipe step model."""
    __tablename__ = 'recipe_steps'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    step_number = db.Column(db.Integer, nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    duration_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    ingredients = db.relationship('RecipeIngredient', backref='step', lazy='dynamic', cascade='all, delete-orphan', order_by='RecipeIngredient.order')

    __table_args__ = (
        db.Index('idx_recipe_step_number', 'recipe_id', 'step_number'),
    )

    def to_dict(self):
        """Serialize step to dictionary."""
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'step_number': self.step_number,
            'instruction': self.instruction,
            'image_url': self.image_url,
            'duration_minutes': self.duration_minutes,
            'ingredients': [ing.to_dict() for ing in self.ingredients.order_by(RecipeIngredient.order).all()],
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<RecipeStep {self.step_number} of recipe {self.recipe_id}>'

