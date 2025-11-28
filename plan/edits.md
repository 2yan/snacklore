# Plan Edits - Aligning with Wireframes

This document outlines necessary edits to align all plan documents with the wireframes, which are the source of truth. The goal is to ensure everything flows together, implements only what's needed, and leads to straightforward success.

## Wireframe Inventory

Based on the wireframes folder, we have:
- `homepage.png` - Homepage
- `recipe_page.png` - Recipe detail page
- `search_page.png` - Search page
- `user_profile.png` - User profile page
- `register_user.png` - User registration
- `top_nav.png` - Top navigation
- `comment_component.png` - Comment component
- `text_editor_recipe.png` - Text-based recipe editor
- `gui_editor_recipe.png` - GUI-based recipe editor

## Critical Issues Found & Corrections

### 1. VOTING SYSTEMS - RECIPES AND COMMENTS

**Wireframe Reality**: Upvotes and downvotes exist at BOTH recipe level AND comment level.

**Decision**: Keep upvote/downvote system for recipes. ADD upvote/downvote system for comments. Remove star ratings entirely.

**Edits Needed**:
- **database.md**: 
  - Remove `ratings` table entirely.
  - Keep `recipe_votes` table (upvote/downvote for recipes).
  - ADD `comment_votes` table (upvote/downvote for comments).
- **api_documentation.md**: 
  - Remove all `/api/recipes/<id>/rate` and `/api/recipes/<id>/rating` endpoints.
  - ADD endpoints for comment voting: `/api/comments/<id>/upvote`, `/api/comments/<id>/downvote`, `/api/comments/<id>/remove-vote`.
- **code_structure.md**: 
  - Remove `models/rating.py`, `routes/ratings.py`.
  - ADD `models/comment_vote.py` and `routes/comment_votes.py`.
- **frontend.md**: 
  - Remove rating display from recipe cards and recipe detail pages.
  - ADD upvote/downvote UI to comment component.

### 2. FAVORITES SYSTEM - MULTI-TYPE

**Wireframe Reality**: Users can favorite other users, recipes, states, OR countries.

**Decision**: Implement a flexible favorites system that supports all four types.

**Edits Needed**:
- **database.md**: 
  - KEEP `favorites` table but expand it to support polymorphic relationships.
  - Structure: `id`, `user_id`, `favorite_type` (enum: 'user', 'recipe', 'state', 'country'), `favorite_id` (integer), `created_at`.
  - Unique constraint on (`user_id`, `favorite_type`, `favorite_id`).
- **api_documentation.md**: 
  - ADD endpoints: 
    - `POST /api/favorites` - Create favorite (with type and id)
    - `DELETE /api/favorites/<id>` - Remove favorite
    - `GET /api/users/<username>/favorites` - Get user's favorites (with filtering by type)
- **code_structure.md**: 
  - KEEP favorites model and routes.
  - Update to handle multiple favorite types.
- **frontend.md**: 
  - ADD favorites functionality to user profiles, recipe pages, state/country pages.

### 3. NESTED COMMENTS - KEEP IT

**Wireframe Reality**: Comments support nesting/replies.

**Decision**: Keep nested comment support via `parent_id`.

**Edits Needed**:
- **database.md**: 
  - KEEP `parent_id` field in `comments` table.
  - KEEP self-referential relationship.
- **api_documentation.md**: 
  - KEEP `parent_id` in comment creation request body.
- **code_structure.md**: 
  - KEEP nested comment handling logic.
- **frontend.md**: 
  - KEEP reply functionality in comment component.

### 4. RECIPE STRUCTURE - STEPS AND INGREDIENTS

**Wireframe Reality**: Recipes have steps, steps have ingredients. Structure: Ingredients → Steps → Recipe → State → Country.

**Decision**: Keep the full structure with separate tables.

**Edits Needed**:
- **database.md**: 
  - KEEP `recipe_steps` table.
  - KEEP `recipe_ingredients` table with `step_id` foreign key.
  - Structure: `recipe_ingredients` → `recipe_steps` → `recipes`.
- **api_documentation.md**: 
  - Recipe creation: Structure ingredients within steps.
  - Format: `steps: [{step_number, instruction, ingredients: [{name, amount, unit}]}]`.
- **code_structure.md**: 
  - KEEP `models/recipe_steps.py`.
  - KEEP `recipe_ingredients` model with step relationship.
- **frontend.md**: 
  - GUI editor: Ingredients are associated with steps.
  - Text editor: Can still use text areas but structure should map to steps/ingredients.

### 5. RECIPES LINKED TO STATES, NOT COUNTRIES

**Wireframe Reality**: Recipes are created at the state level. States are associated with countries. Recipes → State → Country (not direct).

**Decision**: Recipes link to states, states link to countries.

**Edits Needed**:
- **database.md**: 
  - KEEP `countries` table.
  - KEEP `country_states` table (or `states` table).
  - Change `recipes.country_id` to `recipes.state_id` (foreign key to states table).
  - Remove direct country relationship from recipes.
- **api_documentation.md**: 
  - Recipe creation: Use `state_id` instead of `country_id` or `country`.
  - Add endpoints to get states by country.
- **code_structure.md**: 
  - Update recipe model to link to states, not countries.
  - Keep countries and states models.
- **frontend.md**: 
  - Recipe editor: Select state (which implies country).
  - Show breadcrumb: Recipe → State → Country.

### 6. COUNTRIES TABLE - POPULATE FROM STATIC FILE

**Wireframe Reality**: Countries table should exist and be populated from `static/countries.json`.

**Decision**: Keep countries table, populate from JSON file on initialization.

**Edits Needed**:
- **database.md**: 
  - KEEP `countries` table with fields: `id`, `name`, `code` (optional), `continent`, `lat`, `lng`.
  - Add initialization script to populate from `static/countries.json`.
- **api_documentation.md**: 
  - KEEP `/api/countries` endpoints.
  - Add endpoint to get states for a country: `/api/countries/<id>/states`.
- **code_structure.md**: 
  - KEEP `models/countries.py`.
  - Add initialization function to load countries.json into database.
- **frontend.md**: 
  - Country/state selection uses database data (populated from JSON).

### 7. RECIPE METADATA FIELDS - REMOVE

**Problem**: Plans include difficulty, prep_time, cook_time, servings, but not in wireframes.

**Decision**: Remove all metadata fields for MVP.

**Edits Needed**:
- **database.md**: Remove difficulty, prep_time, cook_time, servings from recipes table (if present).
- **api_documentation.md**: Remove these fields from recipe creation/update.
- **frontend.md**: Remove these fields from recipe editor templates.

### 8. RECIPE SLUG - KEEP FOR BREADCRUMBS

**Wireframe Reality**: Slug should be used in breadcrumbs.

**Decision**: Keep slug field for breadcrumb navigation.

**Edits Needed**:
- **database.md**: KEEP `slug` field in recipes table.
- **api_documentation.md**: KEEP slug in recipe responses.
- **code_structure.md**: KEEP slug generation logic.
- **frontend.md**: Use slug in breadcrumbs: Recipe (slug) → State → Country.

### 9. IS_PUBLISHED FLAG - REMOVE

**Problem**: Database has `is_published` boolean flag, not needed for MVP.

**Decision**: Remove. All recipes are published by default in MVP.

**Edits Needed**:
- **database.md**: Remove `is_published` field from recipes table.
- **api_documentation.md**: Remove published filtering.
- **code_structure.md**: Remove published status checks.

### 10. AVATAR_URL - REMOVE

**Problem**: User model includes `avatar_url` but not in wireframes.

**Decision**: Remove for MVP, add later if needed.

**Edits Needed**:
- **database.md**: Remove `avatar_url` from users table.
- **api_documentation.md**: Remove avatar from user profile updates.
- **frontend.md**: Remove avatar display from user profile.

### 11. COMMENT SOFT DELETE - REMOVE

**Problem**: Comments table has `is_deleted` flag for soft deletes.

**Decision**: Use hard deletes for MVP. Simpler.

**Edits Needed**:
- **database.md**: Remove `is_deleted` field from comments table.
- **code_structure.md**: Use actual DELETE instead of soft delete.

### 12. COMMENT IS_EDITED FLAG - KEEP

**Problem**: Comments table has `is_edited` flag.

**Decision**: Keep it - it's simple and useful for UX.

**Edits Needed**: None - keep this.

### 13. SEARCH FILTERS - SIMPLIFY

**Problem**: Frontend plan mentions category filter and difficulty filter, but not in wireframes.

**Decision**: Remove category and difficulty filters. Keep only country/state filter and search query.

**Edits Needed**:
- **frontend.md**: Remove category and difficulty filters from search page description.
- **api_documentation.md**: Remove category and difficulty from search query parameters.
- **code_structure.md**: Remove category and difficulty filtering logic.

### 14. RECIPE IMAGE HANDLING

**Problem**: Plans mention image upload but not clear how images are stored.

**Decision**: For MVP, store image URL as string field. Actual image upload/storage can be simplified (local filesystem or later S3 integration).

**Edits Needed**:
- **database.md**: Add `image_url` VARCHAR field to recipes table (optional).
- **api_documentation.md**: Clarify image handling in recipe creation/update.
- **frontend.md**: Clarify image upload is single image per recipe.

### 15. RECIPE FIELD NAMING - CLARIFICATION

**Problem**: Need to clarify recipe fields.

**Decision**: 
- `title` - Recipe title
- `description` - Short description/summary (optional, for cards)
- `instructions` - Full recipe instructions (markdown/HTML) - NOTE: This is stored at recipe level, but steps are separate
- `slug` - URL-friendly identifier for breadcrumbs

**Edits Needed**:
- **database.md**: 
  - `recipes` table: `id`, `title`, `slug`, `description` (TEXT, optional), `instructions` (TEXT, optional - can be derived from steps), `state_id` (FK), `author_id` (FK), `image_url`, `created_at`, `updated_at`.
- **api_documentation.md**: Clarify field purposes.

## Summary of Required Changes

### Database Schema Updates:
1. ✅ Remove `ratings` table
2. ✅ ADD `comment_votes` table (upvote/downvote for comments)
3. ✅ EXPAND `favorites` table to support users, recipes, states, countries
4. ✅ KEEP `country_states` table (or rename to `states`)
5. ✅ KEEP `countries` table (populate from static/countries.json)
6. ✅ KEEP `recipe_steps` table
7. ✅ KEEP `recipe_ingredients` table with `step_id` FK
8. ✅ KEEP `parent_id` in comments (nested comments)
9. ✅ KEEP `slug` in recipes (for breadcrumbs)
10. ✅ Remove `is_published` from recipes
11. ✅ Remove `avatar_url` from users
12. ✅ Remove `is_deleted` from comments (use hard delete)
13. ✅ Remove difficulty, prep_time, cook_time, servings
14. ✅ Change `recipes.country_id` to `recipes.state_id` (FK to states)
15. ✅ Add `recipes.image_url` VARCHAR field (optional)
16. ✅ Ensure `recipes.instructions` is TEXT field (optional, can derive from steps)

### API Endpoint Changes:
1. ✅ Remove all rating endpoints (`/rate`, `/rating`)
2. ✅ ADD comment voting endpoints (`/comments/<id>/upvote`, `/downvote`, `/remove-vote`)
3. ✅ EXPAND favorites endpoints to support multiple types
4. ✅ KEEP countries endpoints
5. ✅ ADD states endpoints (get states by country)
6. ✅ Update recipe creation to use `state_id` instead of `country_id`
7. ✅ Remove category and difficulty from search filters

### Code Structure Updates:
1. ✅ Remove `models/rating.py`
2. ✅ ADD `models/comment_vote.py`
3. ✅ ADD `routes/comment_votes.py`
4. ✅ KEEP `models/countries.py`
5. ✅ KEEP `models/country_states.py` (or `states.py`)
6. ✅ KEEP `models/recipe_steps.py`
7. ✅ KEEP `recipe_ingredients` model with step relationship
8. ✅ KEEP nested comment logic in `models/comment.py`
9. ✅ Update `models/recipe.py` to link to states (not countries)
10. ✅ Update favorites model to handle multiple types
11. ✅ Add initialization script to populate countries from JSON
12. ✅ Remove category and difficulty filtering from search routes

### Frontend Template Updates:
1. ✅ ADD favorites functionality (users, recipes, states, countries)
2. ✅ Remove rating display from recipe cards/detail
3. ✅ ADD upvote/downvote UI to comments
4. ✅ KEEP reply functionality in comments
5. ✅ Update recipe editor to select state (not country)
6. ✅ ADD breadcrumb navigation (Recipe → State → Country)
7. ✅ Remove difficulty, time, servings fields from recipe editor
8. ✅ Remove avatar display from user profile
9. ✅ Remove category and difficulty filters from search page

## Final Database Schema

### Core Tables (MVP):
1. **users** - id, username, email, password_hash, bio, country, created_at, updated_at
2. **countries** - id, name, code, continent, lat, lng (populated from static/countries.json)
3. **states** - id, country_id (FK), name, created_at
4. **recipes** - id, title, slug, description, instructions, state_id (FK), author_id (FK), image_url, created_at, updated_at
5. **recipe_steps** - id, recipe_id (FK), step_number, instruction, image_url, duration_minutes, created_at
6. **recipe_ingredients** - id, step_id (FK), name, quantity, unit, notes, order, created_at
7. **comments** - id, recipe_id (FK), user_id (FK), parent_id (FK, optional), content, is_edited, created_at, updated_at
8. **recipe_votes** - id, recipe_id (FK), user_id (FK), vote_type (upvote/downvote), created_at, updated_at
9. **comment_votes** - id, comment_id (FK), user_id (FK), vote_type (upvote/downvote), created_at, updated_at
10. **favorites** - id, user_id (FK), favorite_type (user/recipe/state/country), favorite_id (integer), created_at

### Relationships:
- Countries → States (1:N)
- States → Recipes (1:N)
- Users → Recipes (1:N)
- Recipes → Steps (1:N)
- Steps → Ingredients (1:N)
- Users → Comments (1:N)
- Recipes → Comments (1:N)
- Comments → Comments (self-referential, 1:N for replies)
- Users → Recipe Votes (1:N)
- Recipes → Recipe Votes (1:N)
- Users → Comment Votes (1:N)
- Comments → Comment Votes (1:N)
- Users → Favorites (1:N, polymorphic)

## Implementation Priority

1. **Phase 1**: Core models (users, countries, states, recipes, steps, ingredients)
2. **Phase 2**: Authentication and basic CRUD
3. **Phase 3**: Comments and nested replies
4. **Phase 4**: Voting system (recipes and comments)
5. **Phase 5**: Favorites system (multi-type)
6. **Phase 6**: Search and discovery
7. **Phase 7**: Polish and optimization

## Notes

- All changes prioritize alignment with wireframes
- Countries table populated from `static/countries.json` on initialization
- Recipes are created at state level, breadcrumb shows: Recipe → State → Country
- Voting exists for both recipes and comments
- Favorites support users, recipes, states, and countries
- Nested comments are supported
- Recipe structure: Ingredients → Steps → Recipe → State → Country
