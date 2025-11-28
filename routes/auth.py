"""Authentication routes."""
from flask import Blueprint, request, jsonify, session
from db import db
from models.user import User
from utils.auth import login_required, get_current_user
from utils.validators import validate_user_data
from utils.errors import ValidationError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json() or {}
    
    # Validate input
    errors = validate_user_data(data, is_update=False)
    if errors:
        return jsonify({'error': 'ValidationError', 'message': 'Validation failed', 'details': errors}), 400
    
    # Check if username exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Conflict', 'message': 'Username already exists'}), 409
    
    # Check if email exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Conflict', 'message': 'Email already exists'}), 409
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        bio=data.get('bio'),
        country=data.get('country')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'InternalServerError', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and create session."""
    data = request.get_json() or {}
    
    username_or_email = data.get('username')
    password = data.get('password')
    
    if not username_or_email or not password:
        return jsonify({'error': 'BadRequest', 'message': 'Username/email and password required'}), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Unauthorized', 'message': 'Invalid credentials'}), 401
    
    # Create session
    session['user_id'] = user.id
    session.permanent = True
    
    return jsonify(user.to_dict()), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout user and destroy session."""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status."""
    user = get_current_user()
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'error': 'Unauthorized', 'message': 'Not authenticated'}), 401

