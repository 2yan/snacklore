"""Comment vote routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.comment import Comment
from models.comment_vote import CommentVote
from utils.auth import login_required, get_current_user

comment_votes_bp = Blueprint('comment_votes', __name__)


@comment_votes_bp.route('/comments/<int:comment_id>/upvote', methods=['POST'])
@login_required
def upvote_comment(comment_id):
    """Upvote a comment."""
    comment = Comment.query.get_or_404(comment_id)
    current_user = get_current_user()
    
    # Check if vote exists
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    
    if vote:
        # Update existing vote
        vote.vote_type = 'upvote'
    else:
        # Create new vote
        vote = CommentVote(user_id=current_user.id, comment_id=comment_id, vote_type='upvote')
        db.session.add(vote)
    
    try:
        db.session.commit()
        vote_counts = comment.get_vote_counts()
        user_vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
        return jsonify({
            'user_vote': user_vote.vote_type if user_vote else None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@comment_votes_bp.route('/comments/<int:comment_id>/downvote', methods=['POST'])
@login_required
def downvote_comment(comment_id):
    """Downvote a comment."""
    comment = Comment.query.get_or_404(comment_id)
    current_user = get_current_user()
    
    # Check if vote exists
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    
    if vote:
        # Update existing vote
        vote.vote_type = 'downvote'
    else:
        # Create new vote
        vote = CommentVote(user_id=current_user.id, comment_id=comment_id, vote_type='downvote')
        db.session.add(vote)
    
    try:
        db.session.commit()
        vote_counts = comment.get_vote_counts()
        user_vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
        return jsonify({
            'user_vote': user_vote.vote_type if user_vote else None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@comment_votes_bp.route('/comments/<int:comment_id>/remove-vote', methods=['POST'])
@login_required
def remove_comment_vote(comment_id):
    """Remove user's vote from a comment."""
    comment = Comment.query.get_or_404(comment_id)
    current_user = get_current_user()
    
    vote = CommentVote.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    
    if vote:
        try:
            db.session.delete(vote)
            db.session.commit()
            vote_counts = comment.get_vote_counts()
            return jsonify({
                'user_vote': None,
                'upvotes': vote_counts['upvotes'],
                'downvotes': vote_counts['downvotes'],
                'score': vote_counts['score']
            }), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500
    else:
        # No vote to remove, return current counts
        vote_counts = comment.get_vote_counts()
        return jsonify({
            'user_vote': None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200


