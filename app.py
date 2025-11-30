"""Main Flask application."""
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from db import db
from routes import register_blueprints
from models import User, Recipe, Country, CountryState, RecipeStep, RecipeIngredient, Favorite
from utils.auth import get_current_user, login_required
from utils.pagination import get_pagination_params, paginate_query

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres@localhost/snacklore')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# Initialize database
db.init_app(app)

# Register blueprints
register_blueprints(app)

# Context processor to inject current_user into all templates
@app.context_processor
def inject_user():
    return dict(current_user=get_current_user())

@app.route('/')
def index():
    """Homepage route."""
    current_user = get_current_user()
    user_id = current_user.id if current_user else None
    
    # Get featured recipes (simplified: recent recipes)
    featured_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(6).all()
    
    # Get popular recipes (simplified: recent recipes)
    popular_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(10).all()
    
    # Get recent recipes
    recent_recipes = Recipe.query.order_by(Recipe.created_at.desc()).limit(10).all()
    
    # Get countries (limit to top 20 by name for now)
    countries = Country.query.order_by(Country.name.asc()).limit(20).all()
    
    return render_template('home.html', 
                         featured_recipes=featured_recipes,
                         popular_recipes=popular_recipes,
                         recent_recipes=recent_recipes,
                         countries=countries)


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page route."""
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)


@app.route('/search')
def search_page():
    """Search page route."""
    query_str = request.args.get('q', '').strip()
    state_id = request.args.get('state', type=int)
    country_id = request.args.get('country', type=int)
    sort = request.args.get('sort', 'newest')
    page, per_page = get_pagination_params()
    
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
    
    # Apply sorting
    if sort == 'popular':
        # TODO: Implement score sorting
        query = query.order_by(Recipe.created_at.desc())
    else: # newest
        query = query.order_by(Recipe.created_at.desc())
    
    # Paginate
    items, total, pages = paginate_query(query, page, per_page)
    
    # Get countries for filter
    countries = Country.query.order_by(Country.name.asc()).all()
    
    return render_template('search.html', 
                         recipes=items,
                         pagination={'page': page, 'pages': pages, 'has_prev': page > 1, 'has_next': page < pages, 'prev_num': page - 1, 'next_num': page + 1},
                         query=query_str,
                         countries=countries)


@app.route('/user/<username>')
def user_profile_page(username):
    """User profile page route."""
    user = User.query.filter_by(username=username).first_or_404()
    tab = request.args.get('tab', 'recipes')
    
    recipes = []
    if tab == 'recipes':
        recipes = Recipe.query.filter_by(author_id=user.id).order_by(Recipe.created_at.desc()).all()
    elif tab == 'favorites':
        favorites = Favorite.query.filter_by(user_id=user.id).all()
        recipes = [f.recipe for f in favorites]
        
    return render_template('user_profile.html', user=user, recipes=recipes, active_tab=tab)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """Registration page route."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Login page route."""
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        user = User.query.filter(
            (User.username == login) | (User.email == login)
        ).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
            
    return render_template('login.html')


@app.route('/recipe/new', methods=['GET', 'POST'])
@login_required
def new_recipe_page():
    """New recipe page route."""
    if request.method == 'POST':
        mode = request.form.get('mode', 'text')
        title = request.form.get('title')
        description = request.form.get('description')
        state_id = request.form.get('state_id')
        image_url = request.form.get('image_url')
        current_user = get_current_user()
        
        if not title or not state_id:
            flash('Title and State are required', 'error')
            countries = Country.query.order_by(Country.name.asc()).all()
            template = 'recipe_edit_gui.html' if mode == 'gui' else 'recipe_edit.html'
            return render_template(template, countries=countries, recipe=None)
        
        slug = Recipe.generate_slug(title)
        # Ensure slug is unique
        base_slug = slug
        counter = 1
        while Recipe.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        if mode == 'gui':
            # Handle GUI mode with steps
            recipe = Recipe(
                title=title,
                slug=slug,
                description=description,
                author_id=current_user.id,
                state_id=state_id,
                image_url=image_url
            )
            
            try:
                db.session.add(recipe)
                db.session.flush()  # Get recipe.id
                
                # Process steps
                steps_data = {}
                for key, value in request.form.items():
                    if key.startswith('steps['):
                        # Parse key like "steps[0][instruction]" -> step_index=0, field="instruction"
                        import re
                        match = re.match(r'steps\[(\d+)\]\[(\w+)\]', key)
                        if match:
                            step_idx = int(match.group(1))
                            field = match.group(2)
                            if step_idx not in steps_data:
                                steps_data[step_idx] = {}
                            steps_data[step_idx][field] = value
                
                # Process ingredients nested in steps
                for key, value in request.form.items():
                    if 'ingredients' in key:
                        # Parse key like "steps[0][ingredients][0][name]"
                        match = re.match(r'steps\[(\d+)\]\[ingredients\]\[(\d+)\]\[(\w+)\]', key)
                        if match:
                            step_idx = int(match.group(1))
                            ing_idx = int(match.group(2))
                            field = match.group(3)
                            if step_idx not in steps_data:
                                steps_data[step_idx] = {}
                            if 'ingredients' not in steps_data[step_idx]:
                                steps_data[step_idx]['ingredients'] = {}
                            if ing_idx not in steps_data[step_idx]['ingredients']:
                                steps_data[step_idx]['ingredients'][ing_idx] = {}
                            steps_data[step_idx]['ingredients'][ing_idx][field] = value
                
                # Create steps and ingredients
                step_number = 1
                for step_idx in sorted(steps_data.keys()):
                    step_data = steps_data[step_idx]
                    instruction = step_data.get('instruction', '').strip()
                    
                    # Only create step if instruction is provided
                    if instruction:
                        step = RecipeStep(
                            recipe_id=recipe.id,
                            step_number=step_number,
                            instruction=instruction,
                            image_url=step_data.get('image_url') or None,
                            duration_minutes=int(step_data.get('duration')) if step_data.get('duration') else None
                        )
                        db.session.add(step)
                        db.session.flush()  # Get step.id
                        
                        # Create ingredients for this step
                        if 'ingredients' in step_data:
                            ing_order = 0
                            for ing_idx in sorted(step_data['ingredients'].keys()):
                                ing_data = step_data['ingredients'][ing_idx]
                                name = ing_data.get('name', '').strip()
                                
                                # Only create ingredient if name is provided
                                if name:
                                    ingredient = RecipeIngredient(
                                        step_id=step.id,
                                        name=name,
                                        quantity=float(ing_data.get('quantity')) if ing_data.get('quantity') else None,
                                        unit=ing_data.get('unit') or None,
                                        notes=ing_data.get('notes') or None,
                                        order=ing_order
                                    )
                                    db.session.add(ingredient)
                                    ing_order += 1
                        
                        step_number += 1
                
                db.session.commit()
                return redirect(url_for('recipe_detail', recipe_id=recipe.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
        else:
            # Handle text mode
            instructions = request.form.get('instructions')
            recipe = Recipe(
                title=title,
                slug=slug,
                description=description,
                instructions=instructions,
                author_id=current_user.id,
                state_id=state_id,
                image_url=image_url
            )
            
            try:
                db.session.add(recipe)
                db.session.commit()
                return redirect(url_for('recipe_detail', recipe_id=recipe.id))
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'error')
            
    countries = Country.query.order_by(Country.name.asc()).all()
    mode = request.args.get('mode', 'text')
    template = 'recipe_edit_gui.html' if mode == 'gui' else 'recipe_edit.html'
    return render_template(template, countries=countries, recipe=None)


@app.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe_page(recipe_id):
    """Edit recipe page route."""
    recipe = Recipe.query.get_or_404(recipe_id)
    current_user = get_current_user()
    
    if recipe.author_id != current_user.id:
        return "Forbidden", 403
        
    if request.method == 'POST':
        mode = request.form.get('mode', 'text')
        recipe.title = request.form.get('title')
        recipe.description = request.form.get('description')
        recipe.state_id = request.form.get('state_id')
        recipe.image_url = request.form.get('image_url')
        
        if mode == 'gui':
            # Delete existing steps and ingredients (cascade will handle ingredients)
            RecipeStep.query.filter_by(recipe_id=recipe.id).delete()
            
            # Process steps (same logic as new_recipe_page)
            steps_data = {}
            for key, value in request.form.items():
                if key.startswith('steps['):
                    import re
                    match = re.match(r'steps\[(\d+)\]\[(\w+)\]', key)
                    if match:
                        step_idx = int(match.group(1))
                        field = match.group(2)
                        if step_idx not in steps_data:
                            steps_data[step_idx] = {}
                        steps_data[step_idx][field] = value
            
            # Process ingredients nested in steps
            for key, value in request.form.items():
                if 'ingredients' in key:
                    match = re.match(r'steps\[(\d+)\]\[ingredients\]\[(\d+)\]\[(\w+)\]', key)
                    if match:
                        step_idx = int(match.group(1))
                        ing_idx = int(match.group(2))
                        field = match.group(3)
                        if step_idx not in steps_data:
                            steps_data[step_idx] = {}
                        if 'ingredients' not in steps_data[step_idx]:
                            steps_data[step_idx]['ingredients'] = {}
                        if ing_idx not in steps_data[step_idx]['ingredients']:
                            steps_data[step_idx]['ingredients'][ing_idx] = {}
                        steps_data[step_idx]['ingredients'][ing_idx][field] = value
            
            # Create steps and ingredients
            step_number = 1
            for step_idx in sorted(steps_data.keys()):
                step_data = steps_data[step_idx]
                instruction = step_data.get('instruction', '').strip()
                
                # Only create step if instruction is provided
                if instruction:
                    step = RecipeStep(
                        recipe_id=recipe.id,
                        step_number=step_number,
                        instruction=instruction,
                        image_url=step_data.get('image_url') or None,
                        duration_minutes=int(step_data.get('duration')) if step_data.get('duration') else None
                    )
                    db.session.add(step)
                    db.session.flush()  # Get step.id
                    
                    # Create ingredients for this step
                    if 'ingredients' in step_data:
                        ing_order = 0
                        for ing_idx in sorted(step_data['ingredients'].keys()):
                            ing_data = step_data['ingredients'][ing_idx]
                            name = ing_data.get('name', '').strip()
                            
                            # Only create ingredient if name is provided
                            if name:
                                ingredient = RecipeIngredient(
                                    step_id=step.id,
                                    name=name,
                                    quantity=float(ing_data.get('quantity')) if ing_data.get('quantity') else None,
                                    unit=ing_data.get('unit') or None,
                                    notes=ing_data.get('notes') or None,
                                    order=ing_order
                                )
                                db.session.add(ingredient)
                                ing_order += 1
                    
                    step_number += 1
            
            recipe.instructions = None  # Clear text instructions when using steps
        else:
            # Text mode
            recipe.instructions = request.form.get('instructions')
            # Delete steps if switching from GUI to text mode
            RecipeStep.query.filter_by(recipe_id=recipe.id).delete()
        
        try:
            db.session.commit()
            return redirect(url_for('recipe_detail', recipe_id=recipe.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    countries = Country.query.order_by(Country.name.asc()).all()
    mode = request.args.get('mode', 'text')
    template = 'recipe_edit_gui.html' if mode == 'gui' else 'recipe_edit.html'
    return render_template(template, recipe=recipe, countries=countries)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'NotFound', 'message': 'Resource not found'}), 404
    return render_template('base.html', error="Page not found"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'InternalServerError', 'message': 'An internal error occurred'}), 500
    return render_template('base.html', error="Internal Server Error"), 500


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and initialized.")
        except Exception as e:
            print(f"Database connection failed: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
