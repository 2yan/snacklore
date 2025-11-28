"""Recipe Ingredient model."""
from datetime import datetime
from db import db


class RecipeIngredient(db.Model):
    """Recipe ingredient model."""
    __tablename__ = 'recipe_ingredients'

    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('recipe_steps.id', ondelete='CASCADE'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Numeric(10, 2))
    unit = db.Column(db.String(50))
    notes = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_step_order', 'step_id', 'order'),
    )

    def to_dict(self):
        """Serialize ingredient to dictionary."""
        return {
            'id': self.id,
            'step_id': self.step_id,
            'name': self.name,
            'quantity': float(self.quantity) if self.quantity else None,
            'unit': self.unit,
            'notes': self.notes,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<RecipeIngredient {self.name}>'

