# Backend API Documentation

This document outlines all backend methods (routes/endpoints) required for the Snacklore application, based on the wireframes and application requirements.

## Table of Contents
1. [Authentication & User Management](#authentication--user-management)
2. [Recipe Management](#recipe-management)
3. [Search & Discovery](#search--discovery)
4. [Comments & Interactions](#comments--interactions)
5. [User Profiles](#user-profiles)
6. [Homepage & Navigation](#homepage--navigation)
7. [Country & Location](#country--location)

---

## Authentication & User Management

### User Registration
- **POST** `/api/register`
  - **Description**: Register a new user account
  - **Request Body**:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "country": "string (optional)"
    }
    ```
  - **Response**: `201 Created` with user data (excluding password)
  - **Errors**: `400 Bad Request` (validation errors), `409 Conflict` (username/email exists)

### User Login
- **POST** `/api/login`
  - **Description**: Authenticate user and create session
  - **Request Body**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response**: `200 OK` with session token/user data
  - **Errors**: `401 Unauthorized` (invalid credentials)

### User Logout
- **POST** `/api/logout`
  - **Description**: End user session
  - **Authentication**: Required
  - **Response**: `200 OK`
  - **Errors**: `401 Unauthorized` (not logged in)

### Check Authentication Status
- **GET** `/api/auth/status`
  - **Description**: Check if user is authenticated
  - **Response**: `200 OK` with user data if authenticated, `401 Unauthorized` if not

---

## Recipe Management

### Get All Recipes (Paginated)
- **GET** `/api/recipes`
  - **Description**: Retrieve paginated list of recipes
  - **Query Parameters**:
    - `page`: integer (default: 1)
    - `per_page`: integer (default: 20)
    - `sort`: string (options: "newest", "popular", "score", "alphabetical")
    - `state`: integer (filter by state_id)
    - `country`: integer (filter by country_id)
  - **Response**: `200 OK` with paginated recipe list
  ```json
  {
    "recipes": [...],
    "total": integer,
    "page": integer,
    "per_page": integer,
    "pages": integer
  }
  ```

### Get Recipe by ID
- **GET** `/api/recipes/<recipe_id>`
  - **Description**: Retrieve detailed recipe information
  - **Response**: `200 OK` with full recipe data including ingredients, instructions, comments
  - **Errors**: `404 Not Found` (recipe doesn't exist)

### Create Recipe
- **POST** `/api/recipes`
  - **Description**: Create a new recipe
  - **Authentication**: Required
  - **Request Body**:
    ```json
    {
      "title": "string",
      "description": "string (optional)",
      "state_id": integer,
      "image_url": "string (optional)",
      "instructions": "string (optional, markdown or HTML)",
      "steps": [
        {
          "step_number": integer,
          "instruction": "string",
          "image_url": "string (optional)",
          "duration_minutes": integer (optional),
          "ingredients": [
            {
              "name": "string",
              "quantity": number (optional),
              "unit": "string (optional)",
              "notes": "string (optional)",
              "order": integer
            }
          ]
        }
      ]
    }
    ```
  - **Response**: `201 Created` with created recipe data
  - **Errors**: `400 Bad Request` (validation errors), `401 Unauthorized`

### Update Recipe
- **PUT** `/api/recipes/<recipe_id>`
  - **Description**: Update an existing recipe
  - **Authentication**: Required (must be recipe owner)
  - **Request Body**: Same as create recipe
  - **Response**: `200 OK` with updated recipe data
  - **Errors**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

### Delete Recipe
- **DELETE** `/api/recipes/<recipe_id>`
  - **Description**: Delete a recipe
  - **Authentication**: Required (must be recipe owner or admin)
  - **Response**: `204 No Content`
  - **Errors**: `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

### Get Recipe Editor Data
- **GET** `/api/recipes/<recipe_id>/edit`
  - **Description**: Get recipe data for editing (supports both GUI and text editors)
  - **Authentication**: Required (must be recipe owner)
  - **Response**: `200 OK` with recipe data in editable format
  - **Errors**: `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

---

## Search & Discovery

### Search Recipes
- **GET** `/api/search`
  - **Description**: Search recipes by query string
  - **Query Parameters**:
    - `q`: string (search query)
    - `state`: integer (filter by state_id)
    - `country`: integer (filter by country_id)
    - `page`: integer (default: 1)
    - `per_page`: integer (default: 20)
  - **Response**: `200 OK` with search results
  ```json
  {
    "results": [...],
    "total": integer,
    "query": "string",
    "filters": {...}
  }
  ```

### Get Popular Recipes
- **GET** `/api/recipes/popular`
  - **Description**: Get most popular recipes (by upvotes, score, etc.)
  - **Query Parameters**:
    - `limit`: integer (default: 10)
    - `country`: string (optional filter)
  - **Response**: `200 OK` with list of popular recipes

### Get Recent Recipes
- **GET** `/api/recipes/recent`
  - **Description**: Get recently added recipes
  - **Query Parameters**:
    - `limit`: integer (default: 10)
  - **Response**: `200 OK` with list of recent recipes

---

## Comments & Interactions

### Get Recipe Comments
- **GET** `/api/recipes/<recipe_id>/comments`
  - **Description**: Get all comments for a recipe
  - **Query Parameters**:
    - `page`: integer (default: 1)
    - `per_page`: integer (default: 50)
  - **Response**: `200 OK` with paginated comments list
  ```json
  {
    "comments": [
      {
        "id": integer,
        "user": {...},
        "content": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
      }
    ],
    "total": integer
  }
  ```

### Add Comment
- **POST** `/api/recipes/<recipe_id>/comments`
  - **Description**: Add a comment to a recipe
  - **Authentication**: Required
  - **Request Body**:
    ```json
    {
      "content": "string",
      "parent_id": integer (optional, for replies)
    }
    ```
  - **Response**: `201 Created` with comment data
  - **Errors**: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`

### Update Comment
- **PUT** `/api/comments/<comment_id>`
  - **Description**: Update a comment
  - **Authentication**: Required (must be comment owner)
  - **Request Body**:
    ```json
    {
      "content": "string"
    }
    ```
  - **Response**: `200 OK` with updated comment
  - **Errors**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

### Delete Comment
- **DELETE** `/api/comments/<comment_id>`
  - **Description**: Delete a comment
  - **Authentication**: Required (must be comment owner or admin)
  - **Response**: `204 No Content`
  - **Errors**: `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

### Upvote Recipe
- **POST** `/api/recipes/<recipe_id>/upvote`
  - **Description**: Upvote a recipe
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts and user's vote status
  ```json
  {
    "user_vote": "upvote" | "downvote" | null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

### Downvote Recipe
- **POST** `/api/recipes/<recipe_id>/downvote`
  - **Description**: Downvote a recipe
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts and user's vote status
  ```json
  {
    "user_vote": "upvote" | "downvote" | null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

### Remove Vote
- **POST** `/api/recipes/<recipe_id>/remove-vote`
  - **Description**: Remove user's vote from a recipe
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts
  ```json
  {
    "user_vote": null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

### Upvote Comment
- **POST** `/api/comments/<comment_id>/upvote`
  - **Description**: Upvote a comment
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts and user's vote status
  ```json
  {
    "user_vote": "upvote" | "downvote" | null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

### Downvote Comment
- **POST** `/api/comments/<comment_id>/downvote`
  - **Description**: Downvote a comment
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts and user's vote status
  ```json
  {
    "user_vote": "upvote" | "downvote" | null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

### Remove Comment Vote
- **POST** `/api/comments/<comment_id>/remove-vote`
  - **Description**: Remove user's vote from a comment
  - **Authentication**: Required
  - **Response**: `200 OK` with updated vote counts
  ```json
  {
    "user_vote": null,
    "upvotes": integer,
    "downvotes": integer,
    "score": integer
  }
  ```
  - **Errors**: `401 Unauthorized`, `404 Not Found`

---

## Favorites

### Create Favorite
- **POST** `/api/favorites`
  - **Description**: Add a favorite (user, recipe, state, or country)
  - **Authentication**: Required
  - **Request Body**:
    ```json
    {
      "favorite_type": "string (user|recipe|state|country)",
      "favorite_id": integer
    }
    ```
  - **Response**: `201 Created` with favorite data
  - **Errors**: `400 Bad Request`, `401 Unauthorized`, `404 Not Found`

### Remove Favorite
- **DELETE** `/api/favorites/<favorite_id>`
  - **Description**: Remove a favorite
  - **Authentication**: Required (must be favorite owner)
  - **Response**: `204 No Content`
  - **Errors**: `401 Unauthorized`, `403 Forbidden`, `404 Not Found`

### Get User's Favorites
- **GET** `/api/users/<username>/favorites`
  - **Description**: Get user's favorites
  - **Query Parameters**:
    - `type`: string (optional, filter by favorite_type: user|recipe|state|country)
    - `page`: integer (default: 1)
    - `per_page`: integer (default: 20)
  - **Response**: `200 OK` with paginated favorites list
  ```json
  {
    "favorites": [
      {
        "id": integer,
        "favorite_type": "string",
        "favorite_id": integer,
        "favorite_data": {...},
        "created_at": "datetime"
      }
    ],
    "total": integer
  }
  ```

---

## User Profiles

### Get User Profile
- **GET** `/api/users/<username>`
  - **Description**: Get public user profile information
  - **Response**: `200 OK` with user profile data
  ```json
  {
    "username": "string",
    "country": "string",
    "joined_at": "datetime",
    "recipe_count": integer,
    "bio": "string"
  }
  ```
  - **Errors**: `404 Not Found`

### Get User's Recipes
- **GET** `/api/users/<username>/recipes`
  - **Description**: Get all recipes created by a user
  - **Query Parameters**:
    - `page`: integer (default: 1)
    - `per_page`: integer (default: 20)
  - **Response**: `200 OK` with paginated recipe list

### Update User Profile
- **PUT** `/api/users/<username>`
  - **Description**: Update user profile information
  - **Authentication**: Required (must be profile owner)
  - **Request Body**:
    ```json
    {
      "bio": "string",
      "country": "string"
    }
    ```
  - **Response**: `200 OK` with updated profile
  - **Errors**: `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`

### Get Current User Profile
- **GET** `/api/user/profile`
  - **Description**: Get authenticated user's own profile (includes private data)
  - **Authentication**: Required
  - **Response**: `200 OK` with full user profile including email, etc.
  - **Errors**: `401 Unauthorized`

### Update Current User Profile
- **PUT** `/api/user/profile`
  - **Description**: Update authenticated user's own profile
  - **Authentication**: Required
  - **Request Body**: Same as update user profile, plus:
    ```json
    {
      "email": "string",
      "password": "string (optional, for password change)"
    }
    ```
  - **Response**: `200 OK` with updated profile
  - **Errors**: `400 Bad Request`, `401 Unauthorized`

---

## Homepage & Navigation

### Get Homepage Data
- **GET** `/api/home`
  - **Description**: Get data for homepage (featured recipes, popular, recent, etc.)
  - **Response**: `200 OK`
  ```json
  {
    "featured_recipes": [...],
    "popular_recipes": [...],
    "recent_recipes": [...],
    "countries": [...]
  }
  ```

### Get Navigation Data
- **GET** `/api/nav`
  - **Description**: Get navigation menu data (countries, categories, etc.)
  - **Response**: `200 OK`
  ```json
  {
    "countries": [...],
    "user": {...} (if authenticated)
  }
  ```

---

## Country & Location

### Get All Countries
- **GET** `/api/countries`
  - **Description**: Get list of all countries with recipe counts
  - **Response**: `200 OK` with list of countries
  ```json
  [
    {
      "code": "string",
      "name": "string",
      "recipe_count": integer,
      "flag_url": "string"
    }
  ]
  ```

### Get Country Details
- **GET** `/api/countries/<country_id>`
  - **Description**: Get detailed information about a country
  - **Response**: `200 OK` with country data
  - **Errors**: `404 Not Found`

### Get All States
- **GET** `/api/states`
  - **Description**: Get list of all states
  - **Query Parameters**:
    - `country_id`: integer (optional, filter by country)
  - **Response**: `200 OK` with list of states

### Get State Details
- **GET** `/api/states/<state_id>`
  - **Description**: Get detailed information about a state
  - **Response**: `200 OK` with state data
  - **Errors**: `404 Not Found`

---

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**: Invalid request data or validation errors
- **401 Unauthorized**: Authentication required or invalid
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict (e.g., username already exists)
- **500 Internal Server Error**: Server error

### Error Response Format
```json
{
  "error": "string",
  "message": "string",
  "details": {} (optional)
}
```

---

## Authentication

Most endpoints that require authentication will use one of the following methods:

1. **Session-based**: Using Flask sessions (for web interface)
2. **Token-based**: Using JWT tokens (for API access)

Authentication headers:
- **Session**: Cookie-based (automatic with Flask sessions)
- **Token**: `Authorization: Bearer <token>`

---

## Pagination

Endpoints that return lists support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

Response includes pagination metadata:
```json
{
  "items": [...],
  "total": integer,
  "page": integer,
  "per_page": integer,
  "pages": integer
}
```

---

## Notes

- All datetime fields are returned in ISO 8601 format
- All string fields should be validated for length and content
- Rate limiting should be implemented for public endpoints
- CORS headers should be configured appropriately for API access
- Input sanitization is required for all user-generated content (XSS prevention)
- SQL injection prevention is handled by SQLAlchemy ORM
- Vote system: Users can upvote, downvote, or remove their vote. Changing a vote (e.g., from upvote to downvote) should replace the previous vote

