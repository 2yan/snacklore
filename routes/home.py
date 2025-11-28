"""Homepage routes."""
from flask import Blueprint, jsonify
from models.recipe import Recipe
from models.country import Country
from utils.auth import get_current_user

home_bp = Blueprint('home', __name__)


@home_bp.route('/home', methods=['GET'])
def get_homepage():
    """Get homepage data."""
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    # Get featured recipes (simplified: recent recipes)
    featured_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    
    # Get popular recipes (simplified: recent recipes)
    popular_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(10).all()
    
    # Get recent recipes
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(10).all()
    
    # Get countries (limit to top 20 by recipe count for now)
    countries = Country.query.order_by(Country.name.asc()).limit(20).all()
    
    return jsonify({
        'featured_recipes': [r.to_dict(include_steps=False, include_votes=True, user_id=user_id) for r in featured_recipes],
        'popular_recipes': [r.to_dict(include_steps=False, include_votes=True, user_id=user_id) for r in popular_recipes],
        'recent_recipes': [r.to_dict(include_steps=False, include_votes=True, user_id=user_id) for r in recent_recipes],
        'countries': [c.to_dict() for c in countries]
    }), 200


@home_bp.route('/nav', methods=['GET'])
def get_nav():
    """Get navigation menu data."""
    current_user = get_current_user()
    
    # Get countries for navigation
    countries = Country.query.order_by(Country.name.asc()).limit(50).all()
    
    response = {
        'countries': [c.to_dict() for c in countries]
    }
    
    if current_user:
        response['user'] = current_user.to_public_dict()
    
    return jsonify(response), 200

