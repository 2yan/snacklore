#!/usr/bin/env python3
"""
Script to seed countries and states from static/countries.json into the database.
This script should be run after the database tables have been created.
"""

import json
import os
import sys
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

# Database connection parameters
DB_NAME = os.environ.get('POSTGRES_DB', 'snacklore')
DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
DB_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', '')

# Path to countries.json
COUNTRIES_FILE = Path(__file__).parent / "static" / "countries.json"


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


def load_countries_data():
    """Load countries data from JSON file."""
    if not COUNTRIES_FILE.exists():
        print(f"Error: {COUNTRIES_FILE} not found")
        sys.exit(1)
    
    try:
        with open(COUNTRIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} countries from {COUNTRIES_FILE}")
        return data
    except Exception as e:
        print(f"Error loading countries.json: {e}")
        sys.exit(1)


def seed_countries(conn, countries_data):
    """Insert countries into the database."""
    cursor = conn.cursor()
    
    # Check if countries already exist
    cursor.execute("SELECT COUNT(*) FROM countries")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Countries table already has {existing_count} entries. Skipping country seeding.")
        return
    
    # Prepare country data for insertion
    countries_to_insert = []
    for country in countries_data:
        country_name = country.get('country', '').strip()
        if not country_name:
            continue
        
        countries_to_insert.append((
            country_name,
            None,  # code - not in JSON, can be added later
            country.get('continent', '').strip() or None,
            country.get('lat'),
            country.get('lng')
        ))
    
    # Insert countries
    insert_query = """
        INSERT INTO countries (name, code, continent, lat, lng)
        VALUES %s
        ON CONFLICT (name) DO NOTHING
    """
    
    try:
        execute_values(cursor, insert_query, countries_to_insert)
        conn.commit()
        print(f"✓ Inserted {len(countries_to_insert)} countries")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting countries: {e}")
        raise


def seed_states(conn, countries_data):
    """Insert states into the database."""
    cursor = conn.cursor()
    
    # Check if states already exist
    cursor.execute("SELECT COUNT(*) FROM country_states")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"Country_states table already has {existing_count} entries. Skipping state seeding.")
        return
    
    # Get country ID mapping
    cursor.execute("SELECT id, name FROM countries")
    country_map = {name: id for id, name in cursor.fetchall()}
    
    # Prepare state data for insertion
    states_to_insert = []
    states_count = 0
    
    for country in countries_data:
        country_name = country.get('country', '').strip()
        if not country_name:
            continue
        
        country_id = country_map.get(country_name)
        if not country_id:
            print(f"Warning: Country '{country_name}' not found in database, skipping states")
            continue
        
        states = country.get('states', [])
        if not states:
            continue
        
        for state_name in states:
            state_name = state_name.strip()
            if state_name:
                states_to_insert.append((country_id, state_name))
                states_count += 1
    
    # Insert states in batches
    if states_to_insert:
        insert_query = """
            INSERT INTO country_states (country_id, name)
            VALUES %s
            ON CONFLICT (country_id, name) DO NOTHING
        """
        
        try:
            execute_values(cursor, insert_query, states_to_insert)
            conn.commit()
            print(f"✓ Inserted {states_count} states")
        except Exception as e:
            conn.rollback()
            print(f"Error inserting states: {e}")
            raise
    else:
        print("No states to insert")


def main():
    """Main function to seed the database."""
    print("=" * 60)
    print("Seeding Countries and States")
    print("=" * 60)
    print()
    
    # Load countries data
    countries_data = load_countries_data()
    
    # Connect to database
    print("Connecting to database...")
    conn = get_db_connection()
    print("✓ Connected to database")
    print()
    
    try:
        # Seed countries
        print("Seeding countries...")
        seed_countries(conn, countries_data)
        print()
        
        # Seed states
        print("Seeding states...")
        seed_states(conn, countries_data)
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


