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
│   ├── recipe_step.py         # Recipe step model
│   ├── recipe_ingredient.py   # Recipe ingredient model
│   ├── comment.py             # Comment model
│   ├── recipe_vote.py         # Recipe vote model (upvotes/downvotes)
│   ├── comment_vote.py        # Comment vote model (upvotes/downvotes)
│   ├── country.py             # Country model
│   ├── country_state.py       # State model
│   └── favorite.py            # Favorite model (polymorphic)
├── routes/
│   ├── __init__.py            # Blueprint registration
│   ├── auth.py                # Authentication routes
│   ├── recipes.py             # Recipe CRUD routes
│   ├── comments.py            # Comment routes
│   ├── recipe_votes.py        # Recipe vote routes (upvote/downvote)
│   ├── comment_votes.py       # Comment vote routes (upvote/downvote)
│   ├── favorites.py           # Favorites routes
│   ├── users.py               # User profile routes
│   ├── search.py              # Search routes
│   ├── countries.py           # Country routes
│   ├── states.py              # State routes
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
- Countries initialization from static/countries.json

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
- RecipeStep
- RecipeIngredient
- Comment
- RecipeVote
- CommentVote
- Country
- CountryState
- Favorite
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
- Recipe relationships (author, state, steps, comments, recipe_votes, favorites)
- Recipe serialization methods

**Key Fields**:
```python
- id
- title
- slug
- description (optional)
- instructions (optional, markdown/HTML)
- state_id (foreign key to country_states)
- author_id (foreign key to users)
- image_url (optional)
- created_at
- updated_at
```

**Relationships**:
- `author` - Recipe creator
- `state` - State where recipe is from
- `steps` - Recipe steps
- `comments` - Recipe comments
- `recipe_votes` - Upvotes/downvotes
- `favorites` - Users who favorited this recipe

**Methods**:
- `to_dict()` - Full recipe serialization
- `get_score()` - Calculate vote score

---

### `models/recipe_step.py`
**Purpose**: Recipe step database model

**Contents**:
- RecipeStep SQLAlchemy model
- Relationship to recipes and ingredients

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- step_number
- instruction
- image_url (optional)
- duration_minutes (optional)
- created_at
```

**Relationships**:
- `recipe` - Recipe this step belongs to
- `ingredients` - Ingredients for this step

---

### `models/recipe_ingredient.py`
**Purpose**: Recipe ingredient database model

**Contents**:
- RecipeIngredient SQLAlchemy model
- Relationship to recipe steps

**Key Fields**:
```python
- id
- step_id (foreign key)
- name
- quantity (optional)
- unit (optional)
- notes (optional)
- order
- created_at
```

**Relationships**:
- `step` - Recipe step this ingredient belongs to

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
- is_edited
- created_at
- updated_at
```

**Relationships**:
- `user` - Comment author
- `recipe` - Recipe being commented on
- `parent` - Parent comment (for replies)
- `replies` - Child comments
- `comment_votes` - Votes on this comment

---

### `models/recipe_vote.py`
**Purpose**: Recipe vote database model (upvotes/downvotes)

**Contents**:
- RecipeVote SQLAlchemy model
- Unique constraint on (user_id, recipe_id)

**Key Fields**:
```python
- id
- recipe_id (foreign key)
- user_id (foreign key)
- vote_type (enum: 'upvote' or 'downvote')
- created_at
- updated_at
```

**Constraints**:
- Unique (user_id, recipe_id) - one vote per user per recipe

---

### `models/comment_vote.py`
**Purpose**: Comment vote database model (upvotes/downvotes)

**Contents**:
- CommentVote SQLAlchemy model
- Unique constraint on (user_id, comment_id)

**Key Fields**:
```python
- id
- comment_id (foreign key)
- user_id (foreign key)
- vote_type (enum: 'upvote' or 'downvote')
- created_at
- updated_at
```

**Constraints**:
- Unique (user_id, comment_id) - one vote per user per comment

---

### `models/country.py`
**Purpose**: Country database model

**Contents**:
- Country SQLAlchemy model
- Populated from static/countries.json

**Key Fields**:
```python
- id
- name
- code (optional)
- continent
- lat
- lng
- created_at
```

**Relationships**:
- `states` - States in this country
- `favorites` - Users who favorited this country

---

### `models/country_state.py`
**Purpose**: State database model

**Contents**:
- CountryState SQLAlchemy model

**Key Fields**:
```python
- id
- country_id (foreign key)
- name
- created_at
```

**Relationships**:
- `country` - Country this state belongs to
- `recipes` - Recipes from this state
- `favorites` - Users who favorited this state

---

### `models/favorite.py`
**Purpose**: Favorite database model (polymorphic)

**Contents**:
- Favorite SQLAlchemy model
- Supports users, recipes, states, countries

**Key Fields**:
```python
- id
- user_id (foreign key)
- favorite_type (enum: 'user', 'recipe', 'state', 'country')
- favorite_id (integer, polymorphic)
- created_at
```

**Constraints**:
- Unique (user_id, favorite_type, favorite_id) - one favorite per user per type/id

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
- /api/recipes/<id>/upvote, /downvote, /remove-vote -> recipe_votes blueprint
- /api/comments/<id>/upvote, /downvote, /remove-vote -> comment_votes blueprint
- /api/favorites -> favorites blueprint
- /api/users -> users blueprint
- /api/search -> search blueprint
- /api/countries -> countries blueprint
- /api/states -> states blueprint
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
- `models.recipe_step` - Recipe step model
- `models.recipe_ingredient` - Recipe ingredient model
- `models.country_state` - State model

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

### `routes/recipe_votes.py`
**Purpose**: Recipe upvote/downvote routes

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
- `models.recipe_vote` - Recipe vote model
- `models.recipe` - Recipe model

---

### `routes/comment_votes.py`
**Purpose**: Comment upvote/downvote routes

**Routes**:
- `POST /api/comments/<comment_id>/upvote` - Upvote comment
- `POST /api/comments/<comment_id>/downvote` - Downvote comment
- `POST /api/comments/<comment_id>/remove-vote` - Remove vote

**Key Functions**:
- `upvote_comment(comment_id)` - Add/change to upvote
- `downvote_comment(comment_id)` - Add/change to downvote
- `remove_vote(comment_id)` - Remove user's vote

**Dependencies**:
- `utils.auth` - Authentication decorators
- `models.comment_vote` - Comment vote model
- `models.comment` - Comment model

---

### `routes/favorites.py`
**Purpose**: Favorites routes (polymorphic)

**Routes**:
- `POST /api/favorites` - Create favorite
- `DELETE /api/favorites/<favorite_id>` - Remove favorite
- `GET /api/users/<username>/favorites` - Get user's favorites

**Key Functions**:
- `create_favorite()` - Add favorite (user, recipe, state, or country)
- `remove_favorite(favorite_id)` - Remove favorite
- `get_user_favorites(username)` - Get user's favorites with filtering

**Dependencies**:
- `utils.auth` - Authentication decorators
- `utils.pagination` - Pagination helpers
- `models.favorite` - Favorite model

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
- `search_recipes()` - Perform recipe search (by query, state, country)

**Dependencies**:
- `utils.pagination` - Pagination helpers
- `models.recipe` - Recipe model
- `models.country_state` - State model

---

### `routes/countries.py`
**Purpose**: Country-related routes

**Routes**:
- `GET /api/countries` - Get all countries
- `GET /api/countries/<country_id>` - Get country details
- `GET /api/countries/<country_id>/states` - Get states for country
- `GET /api/countries/<country_id>/recipes` - Get recipes by country

**Key Functions**:
- `get_countries()` - List all countries
- `get_country(country_id)` - Get country details
- `get_country_states(country_id)` - Get states for country
- `get_country_recipes(country_id)` - Get recipes for country (via states)

**Dependencies**:
- `utils.pagination` - Pagination helpers
- `models.country` - Country model
- `models.country_state` - State model
- `models.recipe` - Recipe model

---

### `routes/states.py`
**Purpose**: State-related routes

**Routes**:
- `GET /api/states` - Get all states
- `GET /api/states/<state_id>` - Get state details
- `GET /api/states/<state_id>/recipes` - Get recipes by state

**Key Functions**:
- `get_states()` - List all states (with optional country filter)
- `get_state(state_id)` - Get state details
- `get_state_recipes(state_id)` - Get recipes for state

**Dependencies**:
- `utils.pagination` - Pagination helpers
- `models.country_state` - State model
- `models.recipe` - Recipe model

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
- `models.country` - Country model

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
11. `routes/recipe_votes.py` - Recipe voting system
12. `routes/comment_votes.py` - Comment voting system
13. `routes/favorites.py` - Favorites system

### Phase 4: Discovery
14. `routes/search.py` - Search functionality
15. `routes/countries.py` - Country routes
16. `routes/states.py` - State routes
17. `routes/home.py` - Homepage data

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

