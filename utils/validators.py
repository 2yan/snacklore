"""Input validation functions."""
import re
from datetime import datetime


def validate_email(email):
    """Validate email format."""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username):
    """Validate username format."""
    if not username or not isinstance(username, str):
        return False
    # Username: 3-30 chars, alphanumeric and underscores
    pattern = r'^[a-zA-Z0-9_]{3,30}$'
    return bool(re.match(pattern, username))


def validate_recipe_data(data):
    """Validate recipe data."""
    errors = []
    
    if not data.get('title') or not isinstance(data.get('title'), str) or len(data['title'].strip()) == 0:
        errors.append('Title is required')
    elif len(data['title']) > 255:
        errors.append('Title must be 255 characters or less')
    
    if 'state_id' not in data or not isinstance(data.get('state_id'), int):
        errors.append('State ID is required and must be an integer')
    
    if 'description' in data and data['description'] and len(data['description']) > 10000:
        errors.append('Description must be 10000 characters or less')
    
    if 'instructions' in data and data['instructions'] and len(data['instructions']) > 50000:
        errors.append('Instructions must be 50000 characters or less')
    
    return errors


def validate_comment_data(data):
    """Validate comment data."""
    errors = []
    
    if not data.get('content') or not isinstance(data.get('content'), str) or len(data['content'].strip()) == 0:
        errors.append('Content is required')
    elif len(data['content']) > 10000:
        errors.append('Content must be 10000 characters or less')
    
    return errors


def validate_user_data(data, is_update=False):
    """Validate user registration/update data."""
    errors = []
    
    if not is_update:
        if not data.get('username'):
            errors.append('Username is required')
        elif not validate_username(data['username']):
            errors.append('Username must be 3-30 characters, alphanumeric and underscores only')
        
        if not data.get('email'):
            errors.append('Email is required')
        elif not validate_email(data['email']):
            errors.append('Invalid email format')
        
        if not data.get('password'):
            errors.append('Password is required')
        elif len(data['password']) < 6:
            errors.append('Password must be at least 6 characters')
    else:
        if 'email' in data and data['email'] and not validate_email(data['email']):
            errors.append('Invalid email format')
        
        if 'password' in data and data['password'] and len(data['password']) < 6:
            errors.append('Password must be at least 6 characters')
    
    if 'bio' in data and data['bio'] and len(data['bio']) > 1000:
        errors.append('Bio must be 1000 characters or less')
    
    return errors


