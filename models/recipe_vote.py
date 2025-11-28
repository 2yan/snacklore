"""Recipe Vote model."""
from datetime import datetime
from db import db


class RecipeVote(db.Model):
    """Recipe vote model (upvote/downvote)."""
    __tablename__ = 'recipe_votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'recipe_id', name='uq_user_recipe_vote'),
        db.CheckConstraint("vote_type IN ('upvote', 'downvote')", name='check_vote_type'),
    )

    def __repr__(self):
        return f'<RecipeVote {self.vote_type} by user {self.user_id} on recipe {self.recipe_id}>'

