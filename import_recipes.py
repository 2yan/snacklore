#!/usr/bin/env python3
"""
Script to import recipes from JSON format into the Snacklore database.

Usage:
    python import_recipes.py recipes.json
"""

import json
import sys
from app import app, db, Recipe, Step, Ingredient, User, Country, State
from app import generate_slug

def import_recipes(json_file_path):
    """Import recipes from a JSON file into the database."""
    with app.app_context():
        # Load JSON file
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                recipes_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{json_file_path}' not found.")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{json_file_path}': {e}")
            return False
        
        if not isinstance(recipes_data, list):
            print("Error: JSON file must contain an array of recipes.")
            return False
        
        imported_count = 0
        skipped_count = 0
        errors = []
        
        for recipe_data in recipes_data:
            try:
                # Validate required fields
                if 'name' not in recipe_data:
                    errors.append(f"Recipe missing 'name' field: {recipe_data}")
                    skipped_count += 1
                    continue
                
                if 'username' not in recipe_data:
                    errors.append(f"Recipe '{recipe_data.get('name', 'Unknown')}' missing 'username' field")
                    skipped_count += 1
                    continue
                
                # Get or create user
                username = recipe_data['username']
                user = User.query.filter_by(username=username).first()
                if not user:
                    errors.append(f"User '{username}' not found. Recipe '{recipe_data['name']}' skipped.")
                    skipped_count += 1
                    continue
                
                # Get country if specified
                country = None
                if recipe_data.get('country'):
                    country = Country.query.filter(Country.name.ilike(recipe_data['country'])).first()
                    if not country:
                        print(f"Warning: Country '{recipe_data['country']}' not found. Creating it...")
                        country = Country(name=recipe_data['country'])
                        db.session.add(country)
                        db.session.flush()
                
                # Get state if specified
                state = None
                if recipe_data.get('state') and country:
                    state = State.query.filter_by(
                        country_id=country.id,
                        name=recipe_data['state']
                    ).first()
                    if not state:
                        print(f"Warning: State '{recipe_data['state']}' not found in '{country.name}'. Creating it...")
                        state = State(name=recipe_data['state'], country_id=country.id)
                        db.session.add(state)
                        db.session.flush()
                
                # Check if recipe already exists
                existing_recipe = Recipe.query.filter_by(
                    name=recipe_data['name'],
                    user_id=user.id
                ).first()
                
                if existing_recipe:
                    print(f"Recipe '{recipe_data['name']}' by '{username}' already exists. Skipping...")
                    skipped_count += 1
                    continue
                
                # Create recipe
                recipe = Recipe(
                    name=recipe_data['name'],
                    user_id=user.id,
                    primary_country_id=country.id if country else None,
                    primary_state_id=state.id if state else None,
                    slug=generate_slug(username, recipe_data['name'])
                )
                db.session.add(recipe)
                db.session.flush()
                
                # Add steps
                if 'steps' not in recipe_data or not recipe_data['steps']:
                    errors.append(f"Recipe '{recipe_data['name']}' has no steps. Skipping...")
                    db.session.rollback()
                    skipped_count += 1
                    continue
                
                # Sort steps by step_number
                steps_data = sorted(recipe_data['steps'], key=lambda x: x.get('step_number', 0))
                
                for step_data in steps_data:
                    if 'step_number' not in step_data or 'step_text' not in step_data:
                        errors.append(f"Step in recipe '{recipe_data['name']}' missing required fields. Skipping step...")
                        continue
                    
                    step = Step(
                        recipe_id=recipe.id,
                        step_number=step_data['step_number'],
                        step_text=step_data['step_text']
                    )
                    db.session.add(step)
                    db.session.flush()
                    
                    # Add ingredients for this step
                    if 'ingredients' in step_data:
                        for ingredient_data in step_data['ingredients']:
                            if 'name' not in ingredient_data or 'amount' not in ingredient_data:
                                errors.append(f"Ingredient in recipe '{recipe_data['name']}' step {step_data['step_number']} missing required fields. Skipping ingredient...")
                                continue
                            
                            # Use ingredient username or fall back to recipe username
                            ingredient_username = ingredient_data.get('username', username)
                            ingredient_user = User.query.filter_by(username=ingredient_username).first()
                            if not ingredient_user:
                                ingredient_user = user  # Fall back to recipe owner
                            
                            ingredient = Ingredient(
                                step_id=step.id,
                                user_id=ingredient_user.id,
                                name=ingredient_data['name'],
                                amount=ingredient_data['amount']
                            )
                            db.session.add(ingredient)
                
                db.session.commit()
                imported_count += 1
                print(f"✓ Imported recipe: '{recipe_data['name']}' by '{username}'")
                
            except Exception as e:
                db.session.rollback()
                errors.append(f"Error importing recipe '{recipe_data.get('name', 'Unknown')}': {str(e)}")
                skipped_count += 1
                print(f"✗ Error importing recipe '{recipe_data.get('name', 'Unknown')}': {str(e)}")
        
        # Print summary
        print("\n" + "="*50)
        print("Import Summary:")
        print(f"  Successfully imported: {imported_count}")
        print(f"  Skipped/Failed: {skipped_count}")
        if errors:
            print(f"\nErrors/Warnings ({len(errors)}):")
            for error in errors[:10]:  # Show first 10 errors
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        return imported_count > 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python import_recipes.py <recipes.json>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    success = import_recipes(json_file)
    sys.exit(0 if success else 1)

