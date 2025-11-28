"""Comment model."""
from datetime import datetime
from db import db


class Comment(db.Model):
    """Comment model with support for nested replies."""
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), index=True)
    content = db.Column(db.Text, nullable=False)
    is_edited = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic', cascade='all, delete-orphan')
    comment_votes = db.relationship('CommentVote', backref='comment', lazy='dynamic', cascade='all, delete-orphan')

    def get_vote_counts(self):
        """Get upvote and downvote counts."""
        upvotes = self.comment_votes.filter_by(vote_type='upvote').count()
        downvotes = self.comment_votes.filter_by(vote_type='downvote').count()
        return {
            'upvotes': upvotes,
            'downvotes': downvotes,
            'score': upvotes - downvotes
        }

    def to_dict(self, include_replies=True, include_votes=False, user_id=None):
        """Serialize comment to dictionary."""
        data = {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'user_id': self.user_id,
            'user': self.user.to_public_dict() if self.user else None,
            'parent_id': self.parent_id,
            'content': self.content,
            'is_edited': self.is_edited,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_replies:
            data['replies'] = [reply.to_dict(include_replies=False, include_votes=include_votes, user_id=user_id) 
                              for reply in self.replies.order_by(Comment.created_at).all()]

        if include_votes:
            vote_counts = self.get_vote_counts()
            data['upvotes'] = vote_counts['upvotes']
            data['downvotes'] = vote_counts['downvotes']
            data['score'] = vote_counts['score']
            
            # Get user's vote if provided
            if user_id:
                user_vote = self.comment_votes.filter_by(user_id=user_id).first()
                data['user_vote'] = user_vote.vote_type if user_vote else None
            else:
                data['user_vote'] = None

        return data

    def __repr__(self):
        return f'<Comment {self.id}>'

