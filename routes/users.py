"""User profile routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.user import User
from models.recipe import Recipe
from utils.auth import login_required, get_current_user
from utils.validators import validate_user_data
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response

users_bp = Blueprint('users', __name__)


@users_bp.route('/users/<username>', methods=['GET'])
def get_user_profile(username):
    """Get public user profile."""
    user = User.query.filter_by(username=username).first_or_404()
    
    # Get recipe count
    recipe_count = Recipe.query.filter_by(author_id=user.id).count()
    
    profile = user.to_public_dict()
    profile['recipe_count'] = recipe_count
    
    return jsonify(profile), 200


@users_bp.route('/users/<username>', methods=['PUT'])
@login_required
def update_user_profile(username):
    """Update user profile."""
    user = User.query.filter_by(username=username).first_or_404()
    current_user = get_current_user()
    
    # Check permission
    if user.id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to edit this profile'}), 403
    
    data = request.get_json() or {}
    
    # Validate input
    errors = validate_user_data(data, is_update=True)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Update fields
    if 'email' in data:
        # Check if email is already taken
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != user.id:
            return jsonify({'error': 'Conflict', 'message': 'Email already exists'}), 409
        user.email = data['email']
    
    if 'bio' in data:
        user.bio = data['bio']
    
    if 'country' in data:
        user.country = data['country']
    
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@users_bp.route('/users/<username>/recipes', methods=['GET'])
def get_user_recipes(username):
    """Get user's recipes."""
    user = User.query.filter_by(username=username).first_or_404()
    page, per_page = get_pagination_params()
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    query = Recipe.query.filter_by(author_id=user.id)
    query = query.order_by(Recipe.created_at.desc())
    
    items, total, pages = paginate_query(query, page, per_page)
    
    recipes = [recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in items]
    
    return jsonify(format_pagination_response(recipes, total, page, per_page, pages)), 200


@users_bp.route('/user/profile', methods=['GET'])
@login_required
def get_current_profile():
    """Get current user's own profile (includes private data)."""
    current_user = get_current_user()
    return jsonify(current_user.to_dict()), 200


@users_bp.route('/user/profile', methods=['PUT'])
@login_required
def update_current_profile():
    """Update current user's own profile."""
    current_user = get_current_user()
    data = request.get_json() or {}
    
    # Validate input
    errors = validate_user_data(data, is_update=True)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Update fields
    if 'email' in data:
        # Check if email is already taken
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.id != current_user.id:
            return jsonify({'error': 'Conflict', 'message': 'Email already exists'}), 409
        current_user.email = data['email']
    
    if 'bio' in data:
        current_user.bio = data['bio']
    
    if 'country' in data:
        current_user.country = data['country']
    
    if 'password' in data and data['password']:
        current_user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify(current_user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500

