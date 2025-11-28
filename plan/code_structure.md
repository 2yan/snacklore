# Backend Python File Structure Plan

This document outlines the organization and structure of Python files for the Snacklore backend application.

## Directory Structure

```
snacklore/
├── app.py                      # Main application entry point
├── config.py                   # Configuration management
├── models/
│   ├── __init__.py            # Model exports
│   ├── user.py                # User model
│   ├── recipe.py              # Recipe model
│   ├── ingredient.py          # Ingredient model
│   ├── comment.py             # Comment model
│   ├── vote.py                # Vote model (upvotes/downvotes)
│   └── rating.py              # Rating model (star ratings)
├── routes/
│   ├── __init__.py            # Blueprint registration
│   ├── auth.py                # Authentication routes
│   ├── recipes.py             # Recipe CRUD routes
│   ├── comments.py            # Comment routes
│   ├── votes.py               # Vote routes (upvote/downvote)
│   ├── ratings.py             # Rating routes
│   ├── users.py               # User profile routes
│   ├── search.py              # Search routes
│   ├── countries.py           # Country routes
│   └── home.py                # Homepage routes
├── utils/
│   ├── __init__.py
│   ├── auth.py                # Authentication utilities
│   ├── validators.py          # Input validation functions
│   ├── pagination.py          # Pagination helpers
│   ├── errors.py              # Error handling utilities
│   └── sanitizers.py          # Input sanitization
└── requirements.txt           # Python dependencies
```

---

## File Descriptions

### `app.py`
**Purpose**: Main Flask application entry point and initialization

**Contents**:
- Flask app instance creation
- Database initialization
- Blueprint registration
- Error handler registration
- Application startup logic
- Database table creation on startup

**Key Components**:
```python
- Flask app instance
- SQLAlchemy db instance
- Blueprint imports and registration
- Error handlers (404, 500, etc.)
- Database initialization
- CORS configuration (if needed)
- Session configuration
```

**Routes Registered**:
- All blueprints from `routes/` directory

---

### `config.py`
**Purpose**: Application configuration management

**Contents**:
- Configuration classes (Development, Production, Testing)
- Environment variable loading
- Database connection strings
- Secret keys
- Flask configuration settings

**Key Components**:
```python
- Config base class
- DevelopmentConfig
- ProductionConfig
- TestingConfig
- get_config() function to return appropriate config
- Environment variable defaults
```

---

### `models/__init__.py`
**Purpose**: Central export point for all database models

**Contents**:
- Import all models
- Export models for easy importing
- Database relationship setup

**Exports**:
```python
- User
- Recipe
- Ingredient
- Comment
- Vote
- Rating
```

---

### `models/user.py`
**Purpose**: User database model

**Contents**:
- User SQLAlchemy model
- User authentication methods
- Password hashing utilities
- User relationships (recipes, comments, votes)

**Key Fields**:
```python
- id
- username
- email
- password_hash
- country
- bio
- avatar_url
- created_at
- updated_at
```

**Methods**:
- `check_password(password)` - Verify password
- `to_dict()` - Serialize to dictionary
- `to_public_dict()` - Public profile data only

---

### `models/recipe.py`
**Purpose**: Recipe database model

**Contents**:
- Recipe SQLAlchemy model
- Recipe relationships (user, ingredients, comments, votes, ratings)
- Recipe serialization methods

**Key Fields**:
```python
- id
- title
- description
- country
- instructions (markdown/HTML)
- user_id (foreign key)
- created_at
- updated_at
```

**Relationships**:
- `user` - Recipe creator
- `ingredients` - List of ingredients
- `comments` - Recipe comments
- `votes` - Upvotes/downvotes
- `ratings` - Star ratings

**Methods**:
- `to_dict()` - Full recipe serialization
- `get_score()` - Calculate vote score
- `get_average_rating()` - Calculate average rating

---

### `models/ingredient.py`
**Purpose**: Ingredient database model

**Contents**:
- Ingredient SQLAlchemy model
- Relationship to recipes

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- name
- amount
- unit (optional)
- order (for ordering in recipe)
```

---

### `models/comment.py`
**Purpose**: Comment database model

**Contents**:
- Comment SQLAlchemy model
- Support for nested comments (replies)

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- user_id (foreign key)
- parent_id (foreign key, optional for replies)
- content
- created_at
- updated_at
```

**Relationships**:
- `user` - Comment author
- `recipe` - Recipe being commented on
- `parent` - Parent comment (for replies)
- `replies` - Child comments

---

### `models/vote.py`
**Purpose**: Vote database model (upvotes/downvotes)

**Contents**:
- Vote SQLAlchemy model
- Unique constraint on (user_id, recipe_id)

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- user_id (foreign key)
- vote_type (enum: 'upvote' or 'downvote')
- created_at
```

**Constraints**:
- Unique (user_id, recipe_id) - one vote per user per recipe

---

### `models/rating.py`
**Purpose**: Rating database model (star ratings 1-5)

**Contents**:
- Rating SQLAlchemy model
- Unique constraint on (user_id, recipe_id)

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- user_id (foreign key)
- rating (integer 1-5)
- created_at
- updated_at
```

**Constraints**:
- Unique (user_id, recipe_id) - one rating per user per recipe
- Check constraint: rating between 1 and 5

---

### `routes/__init__.py`
**Purpose**: Blueprint registration and route organization

**Contents**:
- Import all route blueprints
- Register blueprints with Flask app
- URL prefix assignments

**Blueprint Registration**:
```python
- /api/auth -> auth blueprint
- /api/recipes -> recipes blueprint
- /api/comments -> comments blueprint
- /api/votes -> votes blueprint
- /api/ratings -> ratings blueprint
- /api/users -> users blueprint
- /api/search -> search blueprint
- /api/countries -> countries blueprint
- /api/home -> home blueprint
```

---

### `routes/auth.py`
**Purpose**: Authentication and user management routes

**Routes**:
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/auth/status` - Check authentication status

**Key Functions**:
- `register()` - Handle user registration
- `login()` - Handle user login
- `logout()` - Handle user logout
- `auth_status()` - Return current user status

**Dependencies**:
- `utils.auth` - Authentication helpers
- `utils.validators` - Input validation
- `models.user` - User model

---

### `routes/recipes.py`
**Purpose**: Recipe CRUD operations

**Routes**:
- `GET /api/recipes` - Get paginated recipes
- `GET /api/recipes/<recipe_id>` - Get recipe by ID
- `POST /api/recipes` - Create recipe
- `PUT /api/recipes/<recipe_id>` - Update recipe
- `DELETE /api/recipes/<recipe_id>` - Delete recipe
- `GET /api/recipes/<recipe_id>/edit` - Get recipe for editing
- `GET /api/recipes/popular` - Get popular recipes
- `GET /api/recipes/recent` - Get recent recipes

**Key Functions**:
- `get_recipes()` - List recipes with pagination and filtering
- `get_recipe(recipe_id)` - Get single recipe
- `create_recipe()` - Create new recipe
- `update_recipe(recipe_id)` - Update existing recipe
- `delete_recipe(recipe_id)` - Delete recipe
- `get_recipe_edit(recipe_id)` - Get recipe for editor
- `get_popular_recipes()` - Get popular recipes
- `get_recent_recipes()` - Get recent recipes

**Dependencies**:
- `utils.auth` - Authentication decorators
- `utils.pagination` - Pagination helpers
- `utils.validators` - Input validation
- `models.recipe` - Recipe model
- `models.ingredient` - Ingredient model

---

### `routes/comments.py`
**Purpose**: Comment management routes

**Routes**:
- `GET /api/recipes/<recipe_id>/comments` - Get recipe comments
- `POST /api/recipes/<recipe_id>/comments` - Add comment
- `PUT /api/comments/<comment_id>` - Update comment
- `DELETE /api/comments/<comment_id>` - Delete comment

**Key Functions**:
- `get_comments(recipe_id)` - Get comments for recipe
- `add_comment(recipe_id)` - Add new comment
- `update_comment(comment_id)` - Update comment
- `delete_comment(comment_id)` - Delete comment

**Dependencies**:
- `utils.auth` - Authentication decorators
- `utils.pagination` - Pagination helpers
- `models.comment` - Comment model

---

### `routes/votes.py`
**Purpose**: Upvote/downvote routes

**Routes**:
- `POST /api/recipes/<recipe_id>/upvote` - Upvote recipe
- `POST /api/recipes/<recipe_id>/downvote` - Downvote recipe
- `POST /api/recipes/<recipe_id>/remove-vote` - Remove vote

**Key Functions**:
- `upvote_recipe(recipe_id)` - Add/change to upvote
- `downvote_recipe(recipe_id)` - Add/change to downvote
- `remove_vote(recipe_id)` - Remove user's vote

**Dependencies**:
- `utils.auth` - Authentication decorators
- `models.vote` - Vote model
- `models.recipe` - Recipe model

---

### `routes/ratings.py`
**Purpose**: Star rating routes

**Routes**:
- `POST /api/recipes/<recipe_id>/rate` - Rate recipe
- `GET /api/recipes/<recipe_id>/rating` - Get rating stats

**Key Functions**:
- `rate_recipe(recipe_id)` - Add/update rating
- `get_rating(recipe_id)` - Get rating statistics

**Dependencies**:
- `utils.auth` - Authentication decorators
- `models.rating` - Rating model
- `models.recipe` - Recipe model

---

### `routes/users.py`
**Purpose**: User profile routes

**Routes**:
- `GET /api/users/<username>` - Get user profile
- `PUT /api/users/<username>` - Update user profile
- `GET /api/users/<username>/recipes` - Get user's recipes
- `GET /api/user/profile` - Get current user profile
- `PUT /api/user/profile` - Update current user profile

**Key Functions**:
- `get_user_profile(username)` - Get public profile
- `update_user_profile(username)` - Update profile
- `get_user_recipes(username)` - Get user's recipes
- `get_current_profile()` - Get own profile
- `update_current_profile()` - Update own profile

**Dependencies**:
- `utils.auth` - Authentication decorators
- `utils.pagination` - Pagination helpers
- `models.user` - User model

---

### `routes/search.py`
**Purpose**: Search functionality

**Routes**:
- `GET /api/search` - Search recipes

**Key Functions**:
- `search_recipes()` - Perform recipe search

**Dependencies**:
- `utils.pagination` - Pagination helpers
- `models.recipe` - Recipe model

---

### `routes/countries.py`
**Purpose**: Country-related routes

**Routes**:
- `GET /api/countries` - Get all countries
- `GET /api/countries/<country_code>` - Get country details
- `GET /api/countries/<country_code>/recipes` - Get recipes by country

**Key Functions**:
- `get_countries()` - List all countries
- `get_country(country_code)` - Get country details
- `get_country_recipes(country_code)` - Get recipes for country

**Dependencies**:
- `utils.pagination` - Pagination helpers
- `models.recipe` - Recipe model
- `static/countries.json` - Country data

---

### `routes/home.py`
**Purpose**: Homepage data routes

**Routes**:
- `GET /api/home` - Get homepage data
- `GET /api/nav` - Get navigation data

**Key Functions**:
- `get_homepage()` - Get homepage data (featured, popular, recent)
- `get_nav()` - Get navigation menu data

**Dependencies**:
- `models.recipe` - Recipe model
- `static/countries.json` - Country data

---

### `utils/auth.py`
**Purpose**: Authentication utilities and decorators

**Contents**:
- `login_required` decorator - Require authentication
- `get_current_user()` - Get current authenticated user
- `hash_password(password)` - Hash password
- `verify_password(password_hash, password)` - Verify password
- Session management helpers

**Key Functions**:
```python
- login_required(f) - Decorator for protected routes
- get_current_user() - Get user from session
- hash_password(password) - Hash password with bcrypt
- verify_password(password_hash, password) - Verify password
```

---

### `utils/validators.py`
**Purpose**: Input validation functions

**Contents**:
- Validation functions for all input types
- Email validation
- Username validation
- Recipe data validation
- Comment validation

**Key Functions**:
```python
- validate_email(email)
- validate_username(username)
- validate_recipe_data(data)
- validate_comment_data(data)
- validate_rating(rating)
```

---

### `utils/pagination.py`
**Purpose**: Pagination helper utilities

**Contents**:
- Pagination calculation functions
- Pagination response formatters

**Key Functions**:
```python
- paginate_query(query, page, per_page)
- format_pagination_response(items, total, page, per_page)
- get_pagination_params(request) - Extract from request
```

---

### `utils/errors.py`
**Purpose**: Error handling utilities

**Contents**:
- Custom exception classes
- Error response formatters
- Error handlers

**Key Functions**:
```python
- format_error_response(error, message, details)
- ValidationError - Custom exception
- NotFoundError - Custom exception
- PermissionError - Custom exception
```

---

### `utils/sanitizers.py`
**Purpose**: Input sanitization for XSS prevention

**Contents**:
- HTML sanitization
- Markdown sanitization
- Text cleaning functions

**Key Functions**:
```python
- sanitize_html(html)
- sanitize_markdown(markdown)
- clean_text(text)
```

---

## Implementation Order

### Phase 1: Foundation
1. `config.py` - Configuration setup
2. `models/` - All database models
3. `utils/auth.py` - Authentication utilities
4. `utils/validators.py` - Basic validation
5. `utils/errors.py` - Error handling

### Phase 2: Core Features
6. `routes/auth.py` - Authentication routes
7. `routes/recipes.py` - Recipe CRUD
8. `routes/users.py` - User profiles
9. `app.py` - Wire everything together

### Phase 3: Interactions
10. `routes/comments.py` - Comments
11. `routes/votes.py` - Voting system
12. `routes/ratings.py` - Ratings

### Phase 4: Discovery
13. `routes/search.py` - Search functionality
14. `routes/countries.py` - Country routes
15. `routes/home.py` - Homepage data

### Phase 5: Polish
16. `utils/pagination.py` - Pagination helpers
17. `utils/sanitizers.py` - Security enhancements
18. Error handlers and edge cases

---

## Dependencies (requirements.txt)

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-CORS==4.0.0
Werkzeug==3.0.1
bcrypt==4.1.2
python-dotenv==1.0.0
psycopg2-binary==2.9.9
```

---

## Notes

- All routes should use Flask blueprints for modularity
- Database models should use SQLAlchemy ORM
- Authentication should use Flask sessions (with option for JWT tokens)
- All user input should be validated and sanitized
- Error responses should follow consistent format
- Pagination should be consistent across all list endpoints
- Database relationships should be properly configured with foreign keys
- Use database indexes on frequently queried fields (user_id, recipe_id, etc.)

