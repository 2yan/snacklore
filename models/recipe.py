"""Recipe model."""
from datetime import datetime
from db import db
import re


class Recipe(db.Model):
    """Recipe model."""
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    state_id = db.Column(db.Integer, db.ForeignKey('country_states.id', ondelete='SET NULL'), nullable=False, index=True)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    steps = db.relationship('RecipeStep', backref='recipe', lazy='dynamic', cascade='all, delete-orphan', order_by='RecipeStep.step_number')
    comments = db.relationship('Comment', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')
    recipe_votes = db.relationship('RecipeVote', backref='recipe', lazy='dynamic', cascade='all, delete-orphan')

    @staticmethod
    def generate_slug(title):
        """Generate URL-friendly slug from title."""
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug[:255]

    def get_score(self):
        """Calculate vote score (upvotes - downvotes)."""
        upvotes = self.recipe_votes.filter_by(vote_type='upvote').count()
        downvotes = self.recipe_votes.filter_by(vote_type='downvote').count()
        return upvotes - downvotes

    def get_vote_counts(self):
        """Get upvote and downvote counts."""
        upvotes = self.recipe_votes.filter_by(vote_type='upvote').count()
        downvotes = self.recipe_votes.filter_by(vote_type='downvote').count()
        return {
            'upvotes': upvotes,
            'downvotes': downvotes,
            'score': upvotes - downvotes
        }

    def to_dict(self, include_steps=True, include_comments=False, include_votes=False, user_id=None):
        """Serialize recipe to dictionary."""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'instructions': self.instructions,
            'author_id': self.author_id,
            'author': self.author.to_public_dict() if self.author else None,
            'state_id': self.state_id,
            'state': self.state.to_dict() if self.state else None,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_steps:
            data['steps'] = [step.to_dict() for step in self.steps.order_by(RecipeStep.step_number).all()]

        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments.filter_by(parent_id=None).order_by(Comment.created_at).all()]

        if include_votes:
            vote_counts = self.get_vote_counts()
            data['upvotes'] = vote_counts['upvotes']
            data['downvotes'] = vote_counts['downvotes']
            data['score'] = vote_counts['score']
            
            # Get user's vote if provided
            if user_id:
                user_vote = self.recipe_votes.filter_by(user_id=user_id).first()
                data['user_vote'] = user_vote.vote_type if user_vote else None
            else:
                data['user_vote'] = None

        return data

    def __repr__(self):
        return f'<Recipe {self.title}>'

