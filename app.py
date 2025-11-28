"""Main Flask application."""
from flask import Flask, render_template, jsonify
from config import get_config
from db import db
from routes import register_blueprints

# Import models to register them with SQLAlchemy
from models import (
    User, Recipe, RecipeStep, RecipeIngredient, Comment,
    RecipeVote, CommentVote, Country, CountryState, Favorite
)

app = Flask(__name__)
app.config.from_object(get_config())

# Initialize database
db.init_app(app)

# Register blueprints
register_blueprints(app)


@app.route('/')
def index():
    """Homepage route."""
    return render_template('home.html')


@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe detail page route."""
    return render_template('recipe_detail.html', recipe_id=recipe_id)


@app.route('/search')
def search_page():
    """Search page route."""
    return render_template('search.html')


@app.route('/user/<username>')
def user_profile_page(username):
    """User profile page route."""
    return render_template('user_profile.html', username=username)


@app.route('/register')
def register_page():
    """Registration page route."""
    return render_template('register.html')


@app.route('/login')
def login_page():
    """Login page route."""
    return render_template('login.html')


@app.route('/recipe/new')
def new_recipe_page():
    """New recipe page route."""
    return render_template('new_recipe.html')


@app.route('/recipe/<int:recipe_id>/edit')
def edit_recipe_page(recipe_id):
    """Edit recipe page route."""
    return render_template('edit_recipe.html', recipe_id=recipe_id)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'NotFound', 'message': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({'error': 'InternalServerError', 'message': 'An internal error occurred'}), 500


if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Database connected and initialized.")
        except Exception as e:
            print(f"Database connection failed: {e}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
