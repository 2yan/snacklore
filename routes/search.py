"""Search routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.recipe import Recipe
from models.country_state import CountryState
from models.country import Country
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response
from utils.auth import get_current_user

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['GET'])
def search_recipes():
    """Search recipes by query string."""
    query_str = request.args.get('q', '').strip()
    state_id = request.args.get('state', type=int)
    country_id = request.args.get('country', type=int)
    page, per_page = get_pagination_params()
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    # Build query
    query = Recipe.query
    
    # Apply search query
    if query_str:
        query = query.filter(
            Recipe.title.ilike(f'%{query_str}%') |
            Recipe.description.ilike(f'%{query_str}%') |
            Recipe.instructions.ilike(f'%{query_str}%')
        )
    
    # Apply filters
    if state_id:
        query = query.filter_by(state_id=state_id)
    elif country_id:
        query = query.join(CountryState).filter(CountryState.country_id == country_id)
    
    # Order by relevance (simplified: by created_at for now)
    query = query.order_by(Recipe.created_at.desc())
    
    # Paginate
    items, total, pages = paginate_query(query, page, per_page)
    
    # Serialize
    recipes = [recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in items]
    
    return jsonify({
        'results': recipes,
        'total': total,
        'query': query_str,
        'filters': {
            'state_id': state_id,
            'country_id': country_id
        },
        'page': page,
        'per_page': per_page,
        'pages': pages
    }), 200


