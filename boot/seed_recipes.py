#!/usr/bin/env python3
"""
Script to seed recipes from static/system_recipes.json into the database.
This script should be run after countries and states have been seeded.
"""

import json
import os
import sys
import re
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values
from werkzeug.security import generate_password_hash

# Database connection parameters
DB_NAME = os.environ.get('POSTGRES_DB', 'snacklore')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

# Path to system_recipes.json (go up one level from boot/ to find static/)
RECIPES_FILE = Path(__file__).parent.parent / "static" / "system_recipes.json"

# System user credentials
SYSTEM_USERNAME = "system"
SYSTEM_EMAIL = "system@snacklore.com"
SYSTEM_PASSWORD = "system_password_change_me"


def generate_slug(title):
    """Generate URL-friendly slug from title."""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:255]


def get_db_connection():
    """Establish connection to PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD if DB_PASSWORD else None
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)


def load_recipes_data():
    """Load recipes data from JSON file."""
    if not RECIPES_FILE.exists():
        print(f"Error: {RECIPES_FILE} not found")
        sys.exit(1)
    
    try:
        with open(RECIPES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} recipes from {RECIPES_FILE}")
        return data
    except Exception as e:
        print(f"Error loading system_recipes.json: {e}")
        sys.exit(1)


def get_or_create_system_user(conn):
    """Get or create system user for recipes."""
    cursor = conn.cursor()
    
    # Check if system user exists
    cursor.execute("SELECT id FROM users WHERE username = %s", (SYSTEM_USERNAME,))
    result = cursor.fetchone()
    
    if result:
        user_id = result[0]
        print(f"Using existing system user (ID: {user_id})")
        return user_id
    
    # Create system user
    password_hash = generate_password_hash(SYSTEM_PASSWORD)
    cursor.execute(
        "INSERT INTO users (username, email, password_hash, bio) VALUES (%s, %s, %s, %s) RETURNING id",
        (SYSTEM_USERNAME, SYSTEM_EMAIL, password_hash, "System account for national dish recipes")
    )
    user_id = cursor.fetchone()[0]
    conn.commit()
    print(f"✓ Created system user (ID: {user_id})")
    return user_id


def get_state_id_for_country(conn, country_name):
    """Get the first state_id for a given country name."""
    cursor = conn.cursor()
    
    # First, get the country_id
    cursor.execute("SELECT id FROM countries WHERE name = %s", (country_name,))
    country_result = cursor.fetchone()
    
    if not country_result:
        print(f"Warning: Country '{country_name}' not found in database")
        return None
    
    country_id = country_result[0]
    
    # Get the first state for this country
    cursor.execute(
        "SELECT id FROM country_states WHERE country_id = %s ORDER BY id LIMIT 1",
        (country_id,)
    )
    state_result = cursor.fetchone()
    
    if not state_result:
        print(f"Warning: No states found for country '{country_name}'")
        return None
    
    return state_result[0]


def seed_recipes(conn, recipes_data):
    """Insert recipes into the database."""
    cursor = conn.cursor()
    
    # Get or create system user
    system_user_id = get_or_create_system_user(conn)
    
    # Check if recipes already exist
    cursor.execute("SELECT COUNT(*) FROM recipes WHERE author_id = %s", (system_user_id,))
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Recipes table already has {existing_count} system recipes. Skipping recipe seeding.")
        return
    
    imported_count = 0
    skipped_count = 0
    errors = []
    
    for recipe_data in recipes_data:
        try:
            country_name = recipe_data.get('country', '').strip()
            if not country_name:
                errors.append("Recipe missing country name")
                skipped_count += 1
                continue
            
            national_dish = recipe_data.get('national_dish', {})
            if not national_dish:
                errors.append(f"Recipe for {country_name} missing national_dish data")
                skipped_count += 1
                continue
            
            title = national_dish.get('title', '').strip()
            if not title:
                errors.append(f"Recipe for {country_name} missing title")
                skipped_count += 1
                continue
            
            # Get state_id for country
            state_id = get_state_id_for_country(conn, country_name)
            if not state_id:
                errors.append(f"Could not find state for country '{country_name}'")
                skipped_count += 1
                continue
            
            # Generate slug
            slug = generate_slug(title)
            base_slug = slug
            counter = 1
            while True:
                cursor.execute("SELECT id FROM recipes WHERE slug = %s", (slug,))
                if not cursor.fetchone():
                    break
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Insert recipe
            description = national_dish.get('description')
            instructions = national_dish.get('instructions')
            image_url = national_dish.get('image_url')
            
            cursor.execute(
                """INSERT INTO recipes (title, slug, description, instructions, author_id, state_id, image_url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (title, slug, description, instructions, system_user_id, state_id, image_url)
            )
            recipe_id = cursor.fetchone()[0]
            
            # Insert steps
            steps = national_dish.get('steps', [])
            if not steps:
                errors.append(f"Recipe '{title}' for {country_name} has no steps")
                conn.rollback()
                skipped_count += 1
                continue
            
            for step_data in steps:
                step_number = step_data.get('step_number')
                instruction = step_data.get('instruction', '').strip()
                
                if not step_number or not instruction:
                    errors.append(f"Step in recipe '{title}' missing required fields")
                    continue
                
                cursor.execute(
                    """INSERT INTO recipe_steps (recipe_id, step_number, instruction, image_url, duration_minutes)
                       VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                    (
                        recipe_id,
                        step_number,
                        instruction,
                        step_data.get('image_url'),
                        step_data.get('duration_minutes')
                    )
                )
                step_id = cursor.fetchone()[0]
                
                # Insert ingredients for this step
                ingredients = step_data.get('ingredients', [])
                for ing_data in ingredients:
                    name = ing_data.get('name', '').strip()
                    if not name:
                        continue
                    
                    cursor.execute(
                        """INSERT INTO recipe_ingredients (step_id, name, quantity, unit, notes, "order")
                           VALUES (%s, %s, %s, %s, %s, %s)""",
                        (
                            step_id,
                            name,
                            ing_data.get('quantity'),
                            ing_data.get('unit'),
                            ing_data.get('notes'),
                            ing_data.get('order', 0)
                        )
                    )
            
            conn.commit()
            imported_count += 1
            if imported_count % 10 == 0:
                print(f"  Imported {imported_count} recipes...")
        
        except Exception as e:
            conn.rollback()
            errors.append(f"Error importing recipe for {recipe_data.get('country', 'Unknown')}: {str(e)}")
            skipped_count += 1
            print(f"✗ Error importing recipe for {recipe_data.get('country', 'Unknown')}: {str(e)}")
    
    print(f"✓ Imported {imported_count} recipes")
    if skipped_count > 0:
        print(f"  Skipped {skipped_count} recipes")
    if errors:
        print(f"\nErrors/Warnings ({len(errors)}):")
        for error in errors[:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")


def main():
    """Main function to seed the database."""
    print("=" * 60)
    print("Seeding National Dish Recipes")
    print("=" * 60)
    print()
    
    # Load recipes data
    recipes_data = load_recipes_data()
    
    # Connect to database
    print("Connecting to database...")
    conn = get_db_connection()
    print("✓ Connected to database")
    print()
    
    try:
        # Seed recipes
        print("Seeding recipes...")
        seed_recipes(conn, recipes_data)
        print()
        
        print("=" * 60)
        print("✓ Seeding completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during seeding: {e}")
        sys.exit(1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

