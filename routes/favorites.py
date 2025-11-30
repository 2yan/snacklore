"""Favorites routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.favorite import Favorite
from models.user import User
from models.recipe import Recipe
from models.country_state import CountryState
from models.country import Country
from utils.auth import login_required, get_current_user
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response

favorites_bp = Blueprint('favorites', __name__)


@favorites_bp.route('/favorites', methods=['POST'])
@login_required
def create_favorite():
    """Add a favorite (user, recipe, state, or country)."""
    data = request.get_json() or {}
    current_user = get_current_user()
    
    favorite_type = data.get('favorite_type')
    favorite_id = data.get('favorite_id')
    
    if not favorite_type or not favorite_id:
        return jsonify({'error': 'BadRequest', 'message': 'favorite_type and favorite_id are required'}), 400
    
    if favorite_type not in ['user', 'recipe', 'state', 'country']:
        return jsonify({'error': 'BadRequest', 'message': 'Invalid favorite_type'}), 400
    
    # Verify the favorite item exists
    if favorite_type == 'user':
        item = User.query.get(favorite_id)
    elif favorite_type == 'recipe':
        item = Recipe.query.get(favorite_id)
    elif favorite_type == 'state':
        item = CountryState.query.get(favorite_id)
    elif favorite_type == 'country':
        item = Country.query.get(favorite_id)
    
    if not item:
        return jsonify({'error': 'NotFound', 'message': f'{favorite_type} not found'}), 404
    
    # Check if favorite already exists
    existing = Favorite.query.filter_by(
        user_id=current_user.id,
        favorite_type=favorite_type,
        favorite_id=favorite_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Conflict', 'message': 'Already favorited'}), 409
    
    # Create favorite
    favorite = Favorite(
        user_id=current_user.id,
        favorite_type=favorite_type,
        favorite_id=favorite_id
    )
    
    try:
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@favorites_bp.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@login_required
def remove_favorite(favorite_id):
    """Remove a favorite."""
    favorite = Favorite.query.get_or_404(favorite_id)
    current_user = get_current_user()
    
    # Check permission
    if favorite.user_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to remove this favorite'}), 403
    
    try:
        db.session.delete(favorite)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@favorites_bp.route('/users/<username>/favorites', methods=['GET'])
def get_user_favorites(username):
    """Get user's favorites."""
    user = User.query.filter_by(username=username).first_or_404()
    page, per_page = get_pagination_params()
    favorite_type = request.args.get('type')
    
    query = Favorite.query.filter_by(user_id=user.id)
    
    if favorite_type:
        if favorite_type not in ['user', 'recipe', 'state', 'country']:
            return jsonify({'error': 'BadRequest', 'message': 'Invalid favorite_type'}), 400
        query = query.filter_by(favorite_type=favorite_type)
    
    query = query.order_by(Favorite.created_at.desc())
    
    items, total, pages = paginate_query(query, page, per_page)
    
    favorites = [favorite.to_dict() for favorite in items]
    
    return jsonify(format_pagination_response(favorites, total, page, per_page, pages)), 200


