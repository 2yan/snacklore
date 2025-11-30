"""Recipe vote routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.recipe import Recipe
from models.recipe_vote import RecipeVote
from utils.auth import login_required, get_current_user

recipe_votes_bp = Blueprint('recipe_votes', __name__)


@recipe_votes_bp.route('/recipes/<int:recipe_id>/upvote', methods=['POST'])
@login_required
def upvote_recipe(recipe_id):
    """Upvote a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    # Check if vote exists
    vote = RecipeVote.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if vote:
        # Update existing vote
        vote.vote_type = 'upvote'
    else:
        # Create new vote
        vote = RecipeVote(user_id=current_user.id, recipe_id=recipe_id, vote_type='upvote')
        db.session.add(vote)
    
    try:
        db.session.commit()
        vote_counts = recipe.get_vote_counts()
        user_vote = RecipeVote.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
        return jsonify({
            'user_vote': user_vote.vote_type if user_vote else None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@recipe_votes_bp.route('/recipes/<int:recipe_id>/downvote', methods=['POST'])
@login_required
def downvote_recipe(recipe_id):
    """Downvote a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    # Check if vote exists
    vote = RecipeVote.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if vote:
        # Update existing vote
        vote.vote_type = 'downvote'
    else:
        # Create new vote
        vote = RecipeVote(user_id=current_user.id, recipe_id=recipe_id, vote_type='downvote')
        db.session.add(vote)
    
    try:
        db.session.commit()
        vote_counts = recipe.get_vote_counts()
        user_vote = RecipeVote.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
        return jsonify({
            'user_vote': user_vote.vote_type if user_vote else None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@recipe_votes_bp.route('/recipes/<int:recipe_id>/remove-vote', methods=['POST'])
@login_required
def remove_recipe_vote(recipe_id):
    """Remove user's vote from a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    vote = RecipeVote.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    
    if vote:
        try:
            db.session.delete(vote)
            db.session.commit()
            vote_counts = recipe.get_vote_counts()
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
        vote_counts = recipe.get_vote_counts()
        return jsonify({
            'user_vote': None,
            'upvotes': vote_counts['upvotes'],
            'downvotes': vote_counts['downvotes'],
            'score': vote_counts['score']
        }), 200


