"""Comment Vote model."""
from datetime import datetime
from db import db


class CommentVote(db.Model):
    """Comment vote model (upvote/downvote)."""
    __tablename__ = 'comment_votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=False, index=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'comment_id', name='uq_user_comment_vote'),
        db.CheckConstraint("vote_type IN ('upvote', 'downvote')", name='check_vote_type'),
    )

    def __repr__(self):
        return f'<CommentVote {self.vote_type} by user {self.user_id} on comment {self.comment_id}>'

