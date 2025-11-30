"""Comment routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.comment import Comment
from models.recipe import Recipe
from utils.auth import login_required, get_current_user
from utils.validators import validate_comment_data
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/recipes/<int:recipe_id>/comments', methods=['GET'])
def get_comments(recipe_id):
    """Get comments for a recipe."""
    # Verify recipe exists
    Recipe.query.get_or_404(recipe_id)
    
    page, per_page = get_pagination_params()
    user_id = get_current_user().id if get_current_user() else None
    
    # Get top-level comments (no parent)
    query = Comment.query.filter_by(recipe_id=recipe_id, parent_id=None)
    query = query.order_by(Comment.created_at.asc())
    
    items, total, pages = paginate_query(query, page, per_page)
    
    comments = [comment.to_dict(include_replies=True, include_votes=True, user_id=user_id) for comment in items]
    
    return jsonify(format_pagination_response(comments, total, page, per_page, pages)), 200


@comments_bp.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
@login_required
def add_comment(recipe_id):
    """Add a comment to a recipe."""
    # Verify recipe exists
    Recipe.query.get_or_404(recipe_id)
    
    data = request.get_json() or {}
    current_user = get_current_user()
    
    # Validate input
    errors = validate_comment_data(data)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Create comment
    comment = Comment(
        recipe_id=recipe_id,
        user_id=current_user.id,
        parent_id=data.get('parent_id'),
        content=data['content']
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        return jsonify(comment.to_dict(include_replies=False, include_votes=True, user_id=current_user.id)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@comments_bp.route('/comments/<int:comment_id>', methods=['PUT'])
@login_required
def update_comment(comment_id):
    """Update a comment."""
    comment = Comment.query.get_or_404(comment_id)
    current_user = get_current_user()
    
    # Check permission
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to edit this comment'}), 403
    
    data = request.get_json() or {}
    
    # Validate input
    errors = validate_comment_data(data)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Update comment
    comment.content = data['content']
    comment.is_edited = True
    
    try:
        db.session.commit()
        return jsonify(comment.to_dict(include_replies=False, include_votes=True, user_id=current_user.id)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@comments_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    """Delete a comment."""
    comment = Comment.query.get_or_404(comment_id)
    current_user = get_current_user()
    
    # Check permission
    if comment.user_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to delete this comment'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


