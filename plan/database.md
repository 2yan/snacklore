# Snacklore Database Schema

## Overview
This document describes all database objects (tables, relationships, and constraints) for the Snacklore application. The database uses PostgreSQL and is managed through SQLAlchemy ORM.

## Database Objects

### 1. Users Table
Stores user account information and profile data.

**Table Name:** `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| `username` | VARCHAR(80) | UNIQUE, NOT NULL | User's chosen username |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| `password_hash` | VARCHAR(255) | NOT NULL | Hashed password (using Werkzeug) |
| `bio` | TEXT | | User biography/description |
| `country` | VARCHAR(100) | | User's country of residence |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last profile update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `username`
- Unique index on `email`
- Index on `created_at` (for sorting)

**Relationships:**
- One-to-many with `recipes` (user can create many recipes)
- One-to-many with `comments` (user can make many comments)
- One-to-many with `favorites` (user can favorite many recipes)
- One-to-many with `recipe_votes` (user can vote on many recipes)

---

### 2. Recipes Table
Stores snack recipe information and content.

**Table Name:** `recipes`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique recipe identifier |
| `title` | VARCHAR(255) | NOT NULL | Recipe title |
| `slug` | VARCHAR(255) | UNIQUE, NOT NULL | URL-friendly identifier |
| `description` | TEXT | | Short description/summary (optional) |
| `instructions` | TEXT | | Full recipe instructions (optional, can derive from steps) |
| `author_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `users.id` |
| `state_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `country_states.id` |
| `image_url` | VARCHAR(500) | | Optional recipe image URL |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Recipe creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `slug`
- Index on `author_id` (foreign key)
- Index on `state_id` (foreign key)
- Index on `created_at` (for sorting)
- Full-text search index on `title` 

**Relationships:**
- Many-to-one with `users` (recipe belongs to one author)
- Many-to-one with `country_states` (recipe associated with one state)
- One-to-many with `comments` (recipe can have many comments)
- One-to-many with `recipe_steps` (recipe has many steps)
- One-to-many with `favorites` (recipe can be favorited by many users)
- One-to-many with `recipe_votes` (recipe can be voted on by many users)

---

### 3. Countries Table
Stores country information for recipe association.

**Table Name:** `countries`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique country identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Country name |
| `code` | VARCHAR(2) | UNIQUE | ISO 3166-1 alpha-2 country code (optional) |
| `continent` | VARCHAR(50) | | Continent name |
| `lat` | DECIMAL(10, 8) | | Geographic latitude |
| `lng` | DECIMAL(11, 8) | | Geographic longitude |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- Primary key on `id`
- Unique index on `name`
- Unique index on `code`
- Index on `continent`

**Relationships:**
- One-to-many with `country_states` (country can have many states/regions)
- One-to-many with `favorites` (country can be favorited by many users)

---

### 4. Country States Table
Stores states/regions within countries.

**Table Name:** `country_states`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique state identifier |
| `country_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `countries.id` |
| `name` | VARCHAR(100) | NOT NULL | State/region name |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- Primary key on `id`
- Index on `country_id` (foreign key)
- Unique constraint on (`country_id`, `name`)

**Relationships:**
- Many-to-one with `countries` (state belongs to one country)
- One-to-many with `recipes` (state can have many recipes)
- One-to-many with `favorites` (state can be favorited by many users)

---

### 5. Comments Table
Stores user comments on recipes.

**Table Name:** `comments`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique comment identifier |
| `recipe_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `recipes.id` |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `users.id` |
| `parent_id` | INTEGER | FOREIGN KEY | Reference to `comments.id` (for nested replies) |
| `content` | TEXT | NOT NULL | Comment text content |
| `is_edited` | BOOLEAN | DEFAULT FALSE | Whether comment was edited |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Comment creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Index on `recipe_id` (foreign key)
- Index on `user_id` (foreign key)
- Index on `parent_id` (foreign key, for nested comments)
- Index on `created_at` (for sorting)

**Relationships:**
- Many-to-one with `recipes` (comment belongs to one recipe)
- Many-to-one with `users` (comment belongs to one user)
- Self-referential: `parent_id` references `comments.id` (for comment threads)
- One-to-many with `comment_votes` (comment can be voted on by many users)

---

### 6. Recipe Ingredients Table
Stores ingredient information for recipe steps. Ingredients must be associated with a step.

**Table Name:** `recipe_ingredients`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique ingredient entry identifier |
| `step_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `recipe_steps.id` |
| `name` | VARCHAR(255) | NOT NULL | Ingredient name |
| `quantity` | DECIMAL(10, 2) | | Ingredient quantity |
| `unit` | VARCHAR(50) | | Measurement unit (e.g., 'cups', 'grams', 'tbsp') |
| `notes` | TEXT | | Additional notes about the ingredient |
| `order` | INTEGER | NOT NULL | Display order within the step |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- Primary key on `id`
- Index on `step_id` (foreign key)
- Index on (`step_id`, `order`) (for sorting)

**Relationships:**
- Many-to-one with `recipe_steps` (ingredient belongs to one step)

---

### 7. Recipe Steps Table
Stores step-by-step instructions for recipes.

**Table Name:** `recipe_steps`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique step identifier |
| `recipe_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `recipes.id` |
| `step_number` | INTEGER | NOT NULL | Step sequence number |
| `instruction` | TEXT | NOT NULL | Step instruction text |
| `image_url` | VARCHAR(500) | | Optional step image URL |
| `duration_minutes` | INTEGER | | Time required for this step |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Record creation timestamp |

**Indexes:**
- Primary key on `id`
- Index on `recipe_id` (foreign key)
- Index on (`recipe_id`, `step_number`) (for sorting)

**Relationships:**
- Many-to-one with `recipes` (step belongs to one recipe)
- One-to-many with `recipe_ingredients` (step can have many ingredients)

---

### 8. Favorites Table
Stores user favorites (users, recipes, states, or countries).

**Table Name:** `favorites`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique favorite identifier |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `users.id` |
| `favorite_type` | VARCHAR(20) | NOT NULL, CHECK (favorite_type IN ('user', 'recipe', 'state', 'country')) | Type of favorite |
| `favorite_id` | INTEGER | NOT NULL | ID of the favorited item (polymorphic) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Favorite creation timestamp |

**Indexes:**
- Primary key on `id`
- Unique constraint on (`user_id`, `favorite_type`, `favorite_id`) (user can only favorite once per type/id)
- Index on `user_id` (foreign key)
- Index on `favorite_type` (for filtering)
- Index on `created_at` (for sorting)

**Relationships:**
- Many-to-one with `users` (favorite belongs to one user)

---

### 9. Recipe Votes Table
Stores user upvotes and downvotes for recipes.

**Table Name:** `recipe_votes`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique vote identifier |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `users.id` |
| `recipe_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `recipes.id` |
| `vote_type` | VARCHAR(10) | NOT NULL, CHECK (vote_type IN ('upvote', 'downvote')) | Type of vote: 'upvote' or 'downvote' |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Vote creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Unique constraint on (`user_id`, `recipe_id`) (user can only vote once per recipe)
- Index on `user_id` (foreign key)
- Index on `recipe_id` (foreign key)
- Index on `vote_type` (for filtering)

**Relationships:**
- Many-to-one with `users` (vote belongs to one user)
- Many-to-one with `recipes` (vote belongs to one recipe)

---

### 10. Comment Votes Table
Stores user upvotes and downvotes for comments.

**Table Name:** `comment_votes`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique vote identifier |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `users.id` |
| `comment_id` | INTEGER | FOREIGN KEY, NOT NULL | Reference to `comments.id` |
| `vote_type` | VARCHAR(10) | NOT NULL, CHECK (vote_type IN ('upvote', 'downvote')) | Type of vote: 'upvote' or 'downvote' |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Vote creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes:**
- Primary key on `id`
- Unique constraint on (`user_id`, `comment_id`) (user can only vote once per comment)
- Index on `user_id` (foreign key)
- Index on `comment_id` (foreign key)
- Index on `vote_type` (for filtering)

**Relationships:**
- Many-to-one with `users` (vote belongs to one user)
- Many-to-one with `comments` (vote belongs to one comment)

---

## Entity Relationship Summary

### Core Entities
1. **Users** - User accounts and profiles
2. **Recipes** - Snack recipes from around the world
3. **Countries** - Geographic locations for recipes
4. **Comments** - User discussions on recipes

### Supporting Entities
5. **Country States** - Sub-regions within countries
6. **Recipe Steps** - Step-by-step instructions for recipes
7. **Recipe Ingredients** - Ingredients associated with recipe steps
8. **Favorites** - User favorites (users, recipes, states, countries)
9. **Recipe Votes** - User upvotes and downvotes on recipes
10. **Comment Votes** - User upvotes and downvotes on comments

## Key Relationships

### User Relationships
- Users → Recipes (1:N) - Users create recipes
- Users → Comments (1:N) - Users make comments
- Users → Favorites (1:N) - Users favorite items (polymorphic)
- Users → Recipe Votes (1:N) - Users vote on recipes
- Users → Comment Votes (1:N) - Users vote on comments

### Recipe Relationships
- Recipes → Users (N:1) - Recipes have authors
- Recipes → Country States (N:1) - Recipes are from states
- Recipes → Comments (1:N) - Recipes have comments
- Recipes → Recipe Steps (1:N) - Recipes have steps
- Recipes → Favorites (1:N) - Recipes are favorited
- Recipes → Recipe Votes (1:N) - Recipes are voted on

### Recipe Step Relationships
- Recipe Steps → Recipes (N:1) - Steps belong to recipes
- Recipe Steps → Recipe Ingredients (1:N) - Steps have ingredients

### Comment Relationships
- Comments → Recipes (N:1) - Comments belong to recipes
- Comments → Users (N:1) - Comments belong to users
- Comments → Comments (N:1, self-referential) - Comments can be replies
- Comments → Comment Votes (1:N) - Comments can be voted on

### Country Relationships
- Countries → Country States (1:N) - Countries have states/regions
- Countries → Favorites (1:N) - Countries can be favorited

## Database Constraints

### Foreign Key Constraints
- All foreign keys use CASCADE DELETE or SET NULL as appropriate
- `recipes.author_id` → `users.id` (CASCADE on user delete)
- `recipes.state_id` → `country_states.id` (SET NULL on state delete)
- `country_states.country_id` → `countries.id` (CASCADE on country delete)
- `comments.recipe_id` → `recipes.id` (CASCADE on recipe delete)
- `comments.user_id` → `users.id` (CASCADE on user delete)
- `comments.parent_id` → `comments.id` (CASCADE on parent delete)
- `recipe_steps.recipe_id` → `recipes.id` (CASCADE on recipe delete)
- `recipe_ingredients.step_id` → `recipe_steps.id` (CASCADE on step delete)
- `recipe_votes.user_id` → `users.id` (CASCADE on user delete)
- `recipe_votes.recipe_id` → `recipes.id` (CASCADE on recipe delete)
- `comment_votes.user_id` → `users.id` (CASCADE on user delete)
- `comment_votes.comment_id` → `comments.id` (CASCADE on comment delete)
- `favorites.user_id` → `users.id` (CASCADE on user delete)

### Unique Constraints
- `users.username` - Unique usernames
- `users.email` - Unique email addresses
- `recipes.slug` - Unique recipe slugs
- `countries.name` - Unique country names
- `favorites(user_id, favorite_type, favorite_id)` - One favorite per user per type/id
- `recipe_votes(user_id, recipe_id)` - One vote per user per recipe
- `comment_votes(user_id, comment_id)` - One vote per user per comment

### Check Constraints
- `recipe_votes.vote_type` - Must be 'upvote' or 'downvote'
- `comment_votes.vote_type` - Must be 'upvote' or 'downvote'
- `favorites.favorite_type` - Must be 'user', 'recipe', 'state', or 'country'

## Indexes

All tables include primary key indexes and foreign key indexes for efficient queries. Additional indexes are defined on:
- Timestamp columns for chronological sorting
- Unique constraint columns
- Frequently queried foreign keys

