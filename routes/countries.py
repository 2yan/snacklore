"""Country routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.country import Country
from models.country_state import CountryState
from models.recipe import Recipe
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response
from utils.auth import get_current_user

countries_bp = Blueprint('countries', __name__)


@countries_bp.route('/countries', methods=['GET'])
def get_countries():
    """Get all countries with recipe counts."""
    countries = Country.query.order_by(Country.name.asc()).all()
    
    result = []
    for country in countries:
        # Count recipes via states
        recipe_count = db.session.query(Recipe).join(CountryState).filter(
            CountryState.country_id == country.id
        ).count()
        
        country_dict = country.to_dict()
        country_dict['recipe_count'] = recipe_count
        result.append(country_dict)
    
    return jsonify(result), 200


@countries_bp.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    """Get country details."""
    country = Country.query.get_or_404(country_id)
    
    # Count recipes via states
    recipe_count = db.session.query(Recipe).join(CountryState).filter(
        CountryState.country_id == country.id
    ).count()
    
    country_dict = country.to_dict()
    country_dict['recipe_count'] = recipe_count
    
    return jsonify(country_dict), 200


@countries_bp.route('/countries/<int:country_id>/states', methods=['GET'])
def get_country_states(country_id):
    """Get states for a country."""
    Country.query.get_or_404(country_id)
    
    states = CountryState.query.filter_by(country_id=country_id).order_by(CountryState.name.asc()).all()
    
    return jsonify([state.to_dict() for state in states]), 200


@countries_bp.route('/countries/<int:country_id>/recipes', methods=['GET'])
def get_country_recipes(country_id):
    """Get recipes for a country (via states)."""
    Country.query.get_or_404(country_id)
    
    page, per_page = get_pagination_params()
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    # Get recipes via states
    query = Recipe.query.join(CountryState).filter(CountryState.country_id == country_id)
    query = query.order_by(Recipe.created_at.desc())
    
    items, total, pages = paginate_query(query, page, per_page)
    
    recipes = [recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in items]
    
    return jsonify(format_pagination_response(recipes, total, page, per_page, pages)), 200

