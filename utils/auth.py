"""Authentication utilities."""
from functools import wraps
from flask import session, jsonify, request, redirect, url_for
from models.user import User


def login_required(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


def get_current_user():
    """Get current authenticated user from session."""
    if 'user_id' not in session:
        return None
    return User.query.get(session['user_id'])


def hash_password(password):
    """Hash password using Werkzeug."""
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """Verify password against hash."""
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)
