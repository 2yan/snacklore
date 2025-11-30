"""Recipe CRUD routes."""
from flask import Blueprint, request, jsonify
from db import db
from models.recipe import Recipe
from models.recipe_step import RecipeStep
from models.recipe_ingredient import RecipeIngredient
from models.country_state import CountryState
from utils.auth import login_required, get_current_user
from utils.validators import validate_recipe_data
from utils.pagination import get_pagination_params, paginate_query, format_pagination_response
from utils.errors import NotFoundError, PermissionError

recipes_bp = Blueprint('recipes', __name__)


@recipes_bp.route('/recipes', methods=['GET'])
def get_recipes():
    """Get paginated list of recipes."""
    page, per_page = get_pagination_params()
    sort = request.args.get('sort', 'newest')
    state_id = request.args.get('state', type=int)
    country_id = request.args.get('country', type=int)
    user_id = get_current_user().id if get_current_user() else None
    
    # Build query
    query = Recipe.query
    
    # Apply filters
    if state_id:
        query = query.filter_by(state_id=state_id)
    elif country_id:
        # Filter by country via states
        query = query.join(CountryState).filter(CountryState.country_id == country_id)
    
    # Apply sorting
    if sort == 'newest':
        query = query.order_by(Recipe.created_at.desc())
    elif sort == 'popular':
        # Sort by score (upvotes - downvotes) - simplified
        query = query.order_by(Recipe.created_at.desc())  # TODO: Implement proper score sorting
    elif sort == 'alphabetical':
        query = query.order_by(Recipe.title.asc())
    else:
        query = query.order_by(Recipe.created_at.desc())
    
    # Paginate
    items, total, pages = paginate_query(query, page, per_page)
    
    # Serialize
    recipes = [recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in items]
    
    return jsonify(format_pagination_response(recipes, total, page, per_page, pages)), 200


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get recipe by ID."""
    user_id = get_current_user().id if get_current_user() else None
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict(include_steps=True, include_comments=True, include_votes=True, user_id=user_id)), 200


@recipes_bp.route('/recipes', methods=['POST'])
@login_required
def create_recipe():
    """Create a new recipe."""
    data = request.get_json() or {}
    current_user = get_current_user()
    
    # Validate input
    errors = validate_recipe_data(data)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Verify state exists
    state = CountryState.query.get(data['state_id'])
    if not state:
        return jsonify({'error': 'NotFound', 'message': 'State not found'}), 404
    
    # Generate slug
    slug = Recipe.generate_slug(data['title'])
    # Ensure slug is unique
    base_slug = slug
    counter = 1
    while Recipe.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Create recipe
    recipe = Recipe(
        title=data['title'],
        slug=slug,
        description=data.get('description'),
        instructions=data.get('instructions'),
        author_id=current_user.id,
        state_id=data['state_id'],
        image_url=data.get('image_url')
    )
    
    try:
        db.session.add(recipe)
        db.session.flush()  # Get recipe.id
        
        # Create steps if provided
        if 'steps' in data and data['steps']:
            for step_data in data['steps']:
                step = RecipeStep(
                    recipe_id=recipe.id,
                    step_number=step_data.get('step_number', 1),
                    instruction=step_data.get('instruction', ''),
                    image_url=step_data.get('image_url'),
                    duration_minutes=step_data.get('duration_minutes')
                )
                db.session.add(step)
                db.session.flush()  # Get step.id
                
                # Create ingredients for this step
                if 'ingredients' in step_data and step_data['ingredients']:
                    for idx, ing_data in enumerate(step_data['ingredients']):
                        ingredient = RecipeIngredient(
                            step_id=step.id,
                            name=ing_data.get('name', ''),
                            quantity=ing_data.get('quantity'),
                            unit=ing_data.get('unit'),
                            notes=ing_data.get('notes'),
                            order=ing_data.get('order', idx)
                        )
                        db.session.add(ingredient)
        
        db.session.commit()
        return jsonify(recipe.to_dict(include_steps=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['PUT'])
@login_required
def update_recipe(recipe_id):
    """Update an existing recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    # Check permission
    if recipe.author_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to edit this recipe'}), 403
    
    data = request.get_json() or {}
    
    # Validate input
    errors = validate_recipe_data(data)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Update recipe fields
    if 'title' in data:
        recipe.title = data['title']
        recipe.slug = Recipe.generate_slug(data['title'])
    if 'description' in data:
        recipe.description = data['description']
    if 'instructions' in data:
        recipe.instructions = data['instructions']
    if 'state_id' in data:
        state = CountryState.query.get(data['state_id'])
        if not state:
            return jsonify({'error': 'NotFound', 'message': 'State not found'}), 404
        recipe.state_id = data['state_id']
    if 'image_url' in data:
        recipe.image_url = data['image_url']
    
    try:
        # Delete existing steps and ingredients
        RecipeStep.query.filter_by(recipe_id=recipe.id).delete()
        
        # Create new steps if provided
        if 'steps' in data and data['steps']:
            for step_data in data['steps']:
                step = RecipeStep(
                    recipe_id=recipe.id,
                    step_number=step_data.get('step_number', 1),
                    instruction=step_data.get('instruction', ''),
                    image_url=step_data.get('image_url'),
                    duration_minutes=step_data.get('duration_minutes')
                )
                db.session.add(step)
                db.session.flush()
                
                if 'ingredients' in step_data and step_data['ingredients']:
                    for idx, ing_data in enumerate(step_data['ingredients']):
                        ingredient = RecipeIngredient(
                            step_id=step.id,
                            name=ing_data.get('name', ''),
                            quantity=ing_data.get('quantity'),
                            unit=ing_data.get('unit'),
                            notes=ing_data.get('notes'),
                            order=ing_data.get('order', idx)
                        )
                        db.session.add(ingredient)
        
        db.session.commit()
        return jsonify(recipe.to_dict(include_steps=True)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@recipes_bp.route('/recipes/<int:recipe_id>', methods=['DELETE'])
@login_required
def delete_recipe(recipe_id):
    """Delete a recipe."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    # Check permission
    if recipe.author_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to delete this recipe'}), 403
    
    try:
        db.session.delete(recipe)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@recipes_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET'])
@login_required
def get_recipe_edit(recipe_id):
    """Get recipe data for editing."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    # Check permission
    if recipe.author_id != current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to edit this recipe'}), 403
    
    return jsonify(recipe.to_dict(include_steps=True)), 200


@recipes_bp.route('/recipes/popular', methods=['GET'])
def get_popular_recipes():
    """Get popular recipes."""
    limit = request.args.get('limit', 10, type=int)
    country = request.args.get('country')
    user_id = get_current_user().id if get_current_user() else None
    
    query = Recipe.query
    
    if country:
        query = query.join(CountryState).join(Country).filter(Country.name == country)
    
    # Simplified: order by created_at for now
    # TODO: Implement proper popularity scoring
    recipes = query.order_by(Recipe.created_at.desc()).limit(limit).all()
    
    return jsonify([recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in recipes]), 200


@recipes_bp.route('/recipes/recent', methods=['GET'])
def get_recent_recipes():
    """Get recent recipes."""
    limit = request.args.get('limit', 10, type=int)
    user_id = get_current_user().id if get_current_user() else None
    
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(limit).all()
    
    return jsonify([recipe.to_dict(include_steps=False, include_votes=True, user_id=user_id) for recipe in recipes]), 200


