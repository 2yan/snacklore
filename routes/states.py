"""State routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.country_state import CountryState
from models.recipe import Recipe
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response
from utils.auth import get_current_user

states_bp = Blueprint('states', __name__)


@states_bp.route('/states', methods=['GET'])
def get_states():
    """Get all states (optionally filtered by country)."""
    country_id = request.args.get('country_id', type=int)
    
    query = CountryState.query
    
    if country_id:
        query = query.filter_by(country_id=country_id)
    
    query = query.order_by(CountryState.name.asc())
    
    states = query.all()
    
    return jsonify([state.to_dict() for state in states]), 200


@states_bp.route('/states/<int:state_id>', methods=['GET'])
def get_state(state_id):
    """Get state details."""
    state = CountryState.query.get_or_404(state_id)
    
    # Count recipes
    recipe_count = Recipe.query.filter_by(state_id=state_id).count()
    
    state_dict = state.to_dict()
    state_dict['recipe_count'] = recipe_count
    
    return jsonify(state_dict), 200


@states_bp.route('/states/<int:state_id>/recipes', methods=['GET'])
def get_state_recipes(state_id):
    """Get recipes for a state."""
    CountryState.query.get_or_404(state_id)
    
    page, per_page = get_pagination_params()
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    query = Recipe.query.filter_by(state_id=state_id)
    query = query.order_by(Recipe.created_at.desc())
    
    items, total, pages = paginate_query(query, page, per_page)
    
    recipes = [recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in items]
    
    return jsonify(format_pagination_response(recipes, total, page, per_page, pages)), 200

