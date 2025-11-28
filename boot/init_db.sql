-- Snacklore Database Initialization Script
-- This script creates all required tables for the Snacklore application

-- Enable UUID extension if needed (for future use)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. USERS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    bio TEXT,
    country VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- ============================================================================
-- 2. COUNTRIES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(2) UNIQUE,
    continent VARCHAR(50),
    lat DECIMAL(10, 8),
    lng DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_countries_continent ON countries(continent);

-- ============================================================================
-- 3. COUNTRY_STATES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS country_states (
    id SERIAL PRIMARY KEY,
    country_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_country_states_country FOREIGN KEY (country_id) 
        REFERENCES countries(id) ON DELETE CASCADE,
    CONSTRAINT uq_country_states_country_name UNIQUE (country_id, name)
);

CREATE INDEX IF NOT EXISTS idx_country_states_country_id ON country_states(country_id);

-- ============================================================================
-- 4. RECIPES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    instructions TEXT,
    author_id INTEGER NOT NULL,
    state_id INTEGER NOT NULL,
    image_url VARCHAR(500),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_recipes_author FOREIGN KEY (author_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_recipes_state FOREIGN KEY (state_id) 
        REFERENCES country_states(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_recipes_author_id ON recipes(author_id);
CREATE INDEX IF NOT EXISTS idx_recipes_state_id ON recipes(state_id);
CREATE INDEX IF NOT EXISTS idx_recipes_created_at ON recipes(created_at);
CREATE INDEX IF NOT EXISTS idx_recipes_slug ON recipes(slug);

-- Full-text search index on title
CREATE INDEX IF NOT EXISTS idx_recipes_title_fts ON recipes USING gin(to_tsvector('english', title));

-- ============================================================================
-- 5. RECIPE_STEPS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS recipe_steps (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction TEXT NOT NULL,
    image_url VARCHAR(500),
    duration_minutes INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_recipe_steps_recipe FOREIGN KEY (recipe_id) 
        REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recipe_steps_recipe_id ON recipe_steps(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_steps_recipe_step ON recipe_steps(recipe_id, step_number);

-- ============================================================================
-- 6. RECIPE_INGREDIENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id SERIAL PRIMARY KEY,
    step_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    quantity DECIMAL(10, 2),
    unit VARCHAR(50),
    notes TEXT,
    "order" INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT fk_recipe_ingredients_step FOREIGN KEY (step_id) 
        REFERENCES recipe_steps(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_step_id ON recipe_ingredients(step_id);
CREATE INDEX IF NOT EXISTS idx_recipe_ingredients_step_order ON recipe_ingredients(step_id, "order");

-- ============================================================================
-- 7. COMMENTS TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    parent_id INTEGER,
    content TEXT NOT NULL,
    is_edited BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_comments_recipe FOREIGN KEY (recipe_id) 
        REFERENCES recipes(id) ON DELETE CASCADE,
    CONSTRAINT fk_comments_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_comments_parent FOREIGN KEY (parent_id) 
        REFERENCES comments(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_comments_recipe_id ON comments(recipe_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON comments(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON comments(parent_id);
CREATE INDEX IF NOT EXISTS idx_comments_created_at ON comments(created_at);

-- ============================================================================
-- 8. FAVORITES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    favorite_type VARCHAR(20) NOT NULL CHECK (favorite_type IN ('user', 'recipe', 'state', 'country')),
    favorite_id INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_favorites_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT uq_favorites_user_type_id UNIQUE (user_id, favorite_type, favorite_id)
);

CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_type ON favorites(favorite_type);
CREATE INDEX IF NOT EXISTS idx_favorites_created_at ON favorites(created_at);

-- ============================================================================
-- 9. RECIPE_VOTES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS recipe_votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    vote_type VARCHAR(10) NOT NULL CHECK (vote_type IN ('upvote', 'downvote')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_recipe_votes_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_recipe_votes_recipe FOREIGN KEY (recipe_id) 
        REFERENCES recipes(id) ON DELETE CASCADE,
    CONSTRAINT uq_recipe_votes_user_recipe UNIQUE (user_id, recipe_id)
);

CREATE INDEX IF NOT EXISTS idx_recipe_votes_user_id ON recipe_votes(user_id);
CREATE INDEX IF NOT EXISTS idx_recipe_votes_recipe_id ON recipe_votes(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_votes_type ON recipe_votes(vote_type);

-- ============================================================================
-- 10. COMMENT_VOTES TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS comment_votes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    comment_id INTEGER NOT NULL,
    vote_type VARCHAR(10) NOT NULL CHECK (vote_type IN ('upvote', 'downvote')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_comment_votes_user FOREIGN KEY (user_id) 
        REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_comment_votes_comment FOREIGN KEY (comment_id) 
        REFERENCES comments(id) ON DELETE CASCADE,
    CONSTRAINT uq_comment_votes_user_comment UNIQUE (user_id, comment_id)
);

CREATE INDEX IF NOT EXISTS idx_comment_votes_user_id ON comment_votes(user_id);
CREATE INDEX IF NOT EXISTS idx_comment_votes_comment_id ON comment_votes(comment_id);
CREATE INDEX IF NOT EXISTS idx_comment_votes_type ON comment_votes(vote_type);

-- ============================================================================
-- END OF TABLE CREATION
-- ============================================================================

