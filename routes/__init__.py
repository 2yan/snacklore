"""Routes package - blueprint registration."""
from flask import Blueprint

# Import all blueprints
from .auth import auth_bp
from .recipes import recipes_bp
from .comments import comments_bp
from .recipe_votes import recipe_votes_bp
from .comment_votes import comment_votes_bp
from .favorites import favorites_bp
from .users import users_bp
from .search import search_bp
from .countries import countries_bp
from .states import states_bp
from .home import home_bp


def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(recipes_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(recipe_votes_bp, url_prefix='/api')
    app.register_blueprint(comment_votes_bp, url_prefix='/api')
    app.register_blueprint(favorites_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(countries_bp, url_prefix='/api')
    app.register_blueprint(states_bp, url_prefix='/api')
    app.register_blueprint(home_bp, url_prefix='/api')

