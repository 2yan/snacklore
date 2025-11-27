from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/snacklore'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    states = db.relationship('State', backref='country', lazy=True)

class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    primary_country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)
    primary_state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)
    primary_country = db.relationship('Country', foreign_keys=[primary_country_id], backref='users')
    primary_state = db.relationship('State', foreign_keys=[primary_state_id], backref='users')
    recipes = db.relationship('Recipe', backref='owner', lazy=True)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    primary_country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=True)
    primary_state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    primary_country = db.relationship('Country', foreign_keys=[primary_country_id], backref='recipes')
    primary_state = db.relationship('State', foreign_keys=[primary_state_id], backref='recipes')
    steps = db.relationship('Step', backref='recipe', lazy=True, order_by='Step.step_number')

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    step_text = db.Column(db.Text, nullable=False)
    ingredients = db.relationship('Ingredient', backref='step', lazy=True, cascade='all, delete-orphan')

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref='ingredients')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('home.html', recipes=recipes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        country_id = request.form.get('country_id')
        state_id = request.form.get('state_id')
        
        if not username or not email or not password:
            flash('All fields are required', 'error')
            countries = Country.query.all()
            return render_template('register.html', countries=countries)
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            countries = Country.query.all()
            return render_template('register.html', countries=countries)
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            countries = Country.query.all()
            return render_template('register.html', countries=countries)
        
        password_hash = generate_password_hash(password)
        user = User(
            username=username, 
            email=email, 
            password_hash=password_hash,
            primary_country_id=int(country_id) if country_id else None,
            primary_state_id=int(state_id) if state_id else None
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    countries = Country.query.all()
    return render_template('register.html', countries=countries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    is_owner = current_user.is_authenticated and recipe.user_id == current_user.id
    countries = Country.query.all()
    states = State.query.all()
    return render_template('recipe.html', recipe=recipe, is_owner=is_owner, countries=countries, states=states)

@app.route('/recipes/<string:recipe_slug>')
def view_recipe_slug(recipe_slug):
    # Convert slug to name (e.g., "miso-ramen" -> "Miso Ramen")
    # This is a simple approximation
    name = recipe_slug.replace('-', ' ').title()
    
    # Try to find case-insensitive match
    recipe = Recipe.query.filter(Recipe.name.ilike(name)).first()
    
    if not recipe:
        # Fallback: try exact match or other variations if needed
        # For now, just 404 if not found
        # Or, specifically for "Miso Ramen" if capitalization differs in DB
        if recipe_slug == 'miso-ramen':
             recipe = Recipe.query.filter(Recipe.name.ilike('Miso Ramen')).first()
        
        if not recipe:
             return "Recipe not found", 404

    # Aggregate ingredients from all steps
    ingredients = []
    if recipe.steps:
        for step in recipe.steps:
            ingredients.extend(step.ingredients)
            
    return render_template('recipe_detail.html', recipe=recipe, ingredients=ingredients, steps=recipe.steps)

@app.route('/countries/<string:country_slug>')
def view_country(country_slug):
    # Convert slug to name (e.g. "japan" -> "Japan", "united-states" -> "United States")
    name = country_slug.replace('-', ' ').title()
    # Handle specific cases if needed, but title() works for most
    if name.lower() == 'usa':
        name = 'United States'
        
    country = Country.query.filter(Country.name.ilike(name)).first()
    
    if not country:
        return "Country not found", 404
        
    recipes = Recipe.query.filter_by(primary_country_id=country.id).all()
    return render_template('country_detail.html', country=country, recipes=recipes)

@app.route('/recipe/<int:recipe_id>/edit', methods=['POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    recipe.name = request.form.get('name', recipe.name)
    country_id = request.form.get('country_id')
    state_id = request.form.get('state_id')
    recipe.primary_country_id = int(country_id) if country_id else None
    recipe.primary_state_id = int(state_id) if state_id else None
    db.session.commit()
    flash('Recipe updated successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/step/<int:step_id>/edit', methods=['POST'])
@login_required
def edit_step(recipe_id, step_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    step = Step.query.get_or_404(step_id)
    if step.recipe_id != recipe_id:
        flash('Step does not belong to this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    step.step_text = request.form.get('step_text', step.step_text)
    db.session.commit()
    flash('Step updated successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/ingredient/<int:ingredient_id>/edit', methods=['POST'])
@login_required
def edit_ingredient(recipe_id, ingredient_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    step = Step.query.get_or_404(ingredient.step_id)
    if step.recipe_id != recipe_id:
        flash('Ingredient does not belong to this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    ingredient.name = request.form.get('name', ingredient.name)
    ingredient.amount = request.form.get('amount', ingredient.amount)
    db.session.commit()
    flash('Ingredient updated successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/step/add', methods=['POST'])
@login_required
def add_step(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    step_text = request.form.get('step_text')
    if not step_text:
        flash('Step text is required', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    # Auto-calculate step number (next available number)
    max_step = db.session.query(db.func.max(Step.step_number)).filter_by(recipe_id=recipe_id).scalar()
    step_number = (max_step or 0) + 1
    
    step = Step(recipe_id=recipe_id, step_number=step_number, step_text=step_text)
    db.session.add(step)
    db.session.commit()
    flash('Step added successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/step/<int:step_id>/delete', methods=['POST'])
@login_required
def delete_step(recipe_id, step_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    step = Step.query.get_or_404(step_id)
    if step.recipe_id != recipe_id:
        flash('Step does not belong to this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    db.session.delete(step)
    db.session.commit()
    flash('Step deleted successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/step/<int:step_id>/ingredient/add', methods=['POST'])
@login_required
def add_ingredient(recipe_id, step_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    step = Step.query.get_or_404(step_id)
    if step.recipe_id != recipe_id:
        flash('Step does not belong to this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    name = request.form.get('name')
    amount = request.form.get('amount')
    if not name or not amount:
        flash('Ingredient name and amount are required', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    ingredient = Ingredient(step_id=step_id, user_id=current_user.id, name=name, amount=amount)
    db.session.add(ingredient)
    db.session.commit()
    flash('Ingredient added successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/recipe/<int:recipe_id>/ingredient/<int:ingredient_id>/delete', methods=['POST'])
@login_required
def delete_ingredient(recipe_id, ingredient_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('You do not have permission to edit this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    ingredient = Ingredient.query.get_or_404(ingredient_id)
    step = Step.query.get_or_404(ingredient.step_id)
    if step.recipe_id != recipe_id:
        flash('Ingredient does not belong to this recipe', 'error')
        return redirect(url_for('view_recipe', recipe_id=recipe_id))
    
    db.session.delete(ingredient)
    db.session.commit()
    flash('Ingredient deleted successfully', 'success')
    return redirect(url_for('view_recipe', recipe_id=recipe_id))

@app.route('/api/states/<int:country_id>')
def get_states(country_id):
    states = State.query.filter_by(country_id=country_id).all()
    return jsonify({'states': [{'id': s.id, 'name': s.name} for s in states]})

@app.route('/recipe/<int:recipe_id>/steps/order', methods=['POST'])
@login_required
def update_step_order(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'}), 403
    
    data = request.get_json()
    step_orders = data.get('step_orders', [])
    
    for order_info in step_orders:
        step = Step.query.get(order_info['step_id'])
        if step and step.recipe_id == recipe_id:
            step.step_number = order_info['step_number']
    
    db.session.commit()
    return jsonify({'success': True})

def init_db():
    """Initialize database with system user, countries, states, and test recipe"""
    # Create System user if it doesn't exist
    system_user = User.query.filter_by(username='System').first()
    if not system_user:
        system_user = User(
            username='System',
            email='system@snacklore.com',
            password_hash=generate_password_hash('systempass')
        )
        db.session.add(system_user)
        db.session.commit()
    
    # Create countries and states if they don't exist
    us = Country.query.filter_by(name='United States').first()
    if not us:
        us = Country(name='United States')
        db.session.add(us)
        db.session.flush()
        
        us_states = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
            'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
            'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
            'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
            'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
            'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon',
            'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
            'West Virginia', 'Wisconsin', 'Wyoming'
        ]
        
        for state_name in us_states:
            state = State(name=state_name, country_id=us.id)
            db.session.add(state)
    
    # Add a few more common countries
    countries_to_add = ['Canada', 'Mexico', 'United Kingdom', 'France', 'Germany', 'Japan', 'China', 'Australia']
    for country_name in countries_to_add:
        country = Country.query.filter_by(name=country_name).first()
        if not country:
            country = Country(name=country_name)
            db.session.add(country)
    
    db.session.commit()
    
    # Create test recipe if it doesn't exist
    test_recipe = Recipe.query.filter_by(name='Test Recipe').first()
    if not test_recipe:
        # Get US and California for the test recipe
        us = Country.query.filter_by(name='United States').first()
        california = State.query.filter_by(name='California').first()
        
        test_recipe = Recipe(
            name='Test Recipe',
            user_id=system_user.id,
            primary_country_id=us.id if us else None,
            primary_state_id=california.id if california else None
        )
        db.session.add(test_recipe)
        db.session.flush()
        
        # Add steps with ingredients
        step1 = Step(
            recipe_id=test_recipe.id,
            step_number=1,
            step_text='Gather all ingredients and prepare your workspace.'
        )
        db.session.add(step1)
        db.session.flush()
        
        ingredient1 = Ingredient(
            step_id=step1.id,
            user_id=system_user.id,
            name='Flour',
            amount='2 cups'
        )
        ingredient2 = Ingredient(
            step_id=step1.id,
            user_id=system_user.id,
            name='Sugar',
            amount='1 cup'
        )
        db.session.add(ingredient1)
        db.session.add(ingredient2)
        
        step2 = Step(
            recipe_id=test_recipe.id,
            step_number=2,
            step_text='Mix the dry ingredients together in a large bowl.'
        )
        db.session.add(step2)
        db.session.flush()
        
        ingredient3 = Ingredient(
            step_id=step2.id,
            user_id=system_user.id,
            name='Baking Powder',
            amount='1 tablespoon'
        )
        db.session.add(ingredient3)
        
        step3 = Step(
            recipe_id=test_recipe.id,
            step_number=3,
            step_text='Add wet ingredients and mix until smooth.'
        )
        db.session.add(step3)
        db.session.flush()
        
        ingredient4 = Ingredient(
            step_id=step3.id,
            user_id=system_user.id,
            name='Eggs',
            amount='2 large'
        )
        ingredient5 = Ingredient(
            step_id=step3.id,
            user_id=system_user.id,
            name='Milk',
            amount='1 cup'
        )
        db.session.add(ingredient4)
        db.session.add(ingredient5)
        
        db.session.commit()

    # Create Miso Ramen recipe if it doesn't exist
    miso_ramen = Recipe.query.filter_by(name='Miso Ramen').first()
    if not miso_ramen:
        japan = Country.query.filter_by(name='Japan').first()
        if not japan:
            japan = Country(name='Japan')
            db.session.add(japan)
            db.session.flush()
            
        miso_ramen = Recipe(
            name='Miso Ramen',
            user_id=system_user.id,
            primary_country_id=japan.id,
            primary_state_id=None
        )
        db.session.add(miso_ramen)
        db.session.flush()
        
        # Step 1: Broth
        step1 = Step(
            recipe_id=miso_ramen.id,
            step_number=1,
            step_text='Prepare the broth base. In a pot, combine chicken stock and dashi. Bring to a simmer.'
        )
        db.session.add(step1)
        db.session.flush()
        
        ing1 = Ingredient(step_id=step1.id, user_id=system_user.id, name='Chicken Stock', amount='4 cups')
        ing2 = Ingredient(step_id=step1.id, user_id=system_user.id, name='Dashi', amount='1 cup')
        db.session.add(ing1)
        db.session.add(ing2)
        
        # Step 2: Miso Taré
        step2 = Step(
            recipe_id=miso_ramen.id,
            step_number=2,
            step_text='Make the Miso Taré. Mix miso paste, sake, mirin, and soy sauce in a small bowl until smooth. Add to the simmering broth.'
        )
        db.session.add(step2)
        db.session.flush()
        
        ing3 = Ingredient(step_id=step2.id, user_id=system_user.id, name='Red Miso', amount='3 tbsp')
        ing4 = Ingredient(step_id=step2.id, user_id=system_user.id, name='Sake', amount='1 tbsp')
        ing5 = Ingredient(step_id=step2.id, user_id=system_user.id, name='Mirin', amount='1 tbsp')
        db.session.add(ing3)
        db.session.add(ing4)
        db.session.add(ing5)
        
        # Step 3: Noodles
        step3 = Step(
            recipe_id=miso_ramen.id,
            step_number=3,
            step_text='Cook the ramen noodles according to package instructions. Drain well.'
        )
        db.session.add(step3)
        db.session.flush()
        
        ing6 = Ingredient(step_id=step3.id, user_id=system_user.id, name='Fresh Ramen Noodles', amount='2 portions')
        db.session.add(ing6)
        
        # Step 4: Assemble
        step4 = Step(
            recipe_id=miso_ramen.id,
            step_number=4,
            step_text='Assemble the bowl. Place noodles in bowl, pour over hot broth. Top with chashu pork, soft boiled egg, corn, and green onions.'
        )
        db.session.add(step4)
        db.session.flush()
        
        ing7 = Ingredient(step_id=step4.id, user_id=system_user.id, name='Chashu Pork', amount='4 slices')
        ing8 = Ingredient(step_id=step4.id, user_id=system_user.id, name='Soft Boiled Egg', amount='2 halves')
        ing9 = Ingredient(step_id=step4.id, user_id=system_user.id, name='Corn', amount='1/4 cup')
        ing10 = Ingredient(step_id=step4.id, user_id=system_user.id, name='Green Onions', amount='2 tbsp, chopped')
        db.session.add(ing7)
        db.session.add(ing8)
        db.session.add(ing9)
        db.session.add(ing10)
        
        db.session.commit()
    
    # Add more Japanese recipes for the country hub
    japan = Country.query.filter_by(name='Japan').first()
    if japan:
        jp_recipes = [
            'Sushi Rolls', 'Tempura', 'Udon Noodle Soup', 
            'Okonomiyaki', 'Yakitori', 'Matcha Green Tea Cake', 'Teriyaki Chicken'
        ]
        for r_name in jp_recipes:
            if not Recipe.query.filter_by(name=r_name).first():
                r = Recipe(name=r_name, user_id=system_user.id, primary_country_id=japan.id)
                db.session.add(r)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
