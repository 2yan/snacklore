#!/usr/bin/env python3
"""
Script to update states in static/countries.json with data from
https://github.com/dr5hn/countries-states-cities-database/blob/master/json/countries%2Bstates.json
"""

import json
import urllib.request
import os
from pathlib import Path

# URL to fetch the countries+states data
GITHUB_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/json/countries%2Bstates.json"

# Path to the local countries.json file
LOCAL_COUNTRIES_FILE = Path(__file__).parent / "static" / "countries.json"
BACKUP_FILE = Path(__file__).parent / "static" / "countries.json.backup"


def fetch_github_data():
    """Fetch the countries+states data from GitHub."""
    print(f"Fetching data from {GITHUB_URL}...")
    try:
        with urllib.request.urlopen(GITHUB_URL) as response:
            data = json.loads(response.read().decode('utf-8'))
        print(f"✓ Successfully fetched data for {len(data)} countries")
        return data
    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        return None


def load_local_countries():
    """Load the local countries.json file."""
    print(f"Loading local countries file from {LOCAL_COUNTRIES_FILE}...")
    try:
        with open(LOCAL_COUNTRIES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data)} countries from local file")
        return data
    except Exception as e:
        print(f"✗ Error loading local file: {e}")
        return None


def create_backup():
    """Create a backup of the current countries.json file."""
    if LOCAL_COUNTRIES_FILE.exists():
        print(f"Creating backup at {BACKUP_FILE}...")
        try:
            import shutil
            shutil.copy2(LOCAL_COUNTRIES_FILE, BACKUP_FILE)
            print(f"✓ Backup created successfully")
            return True
        except Exception as e:
            print(f"✗ Error creating backup: {e}")
            return False
    return False


def normalize_country_name(name):
    """Normalize country name for comparison (lowercase, strip whitespace)."""
    return name.lower().strip() if name else ""


def update_states(local_countries, github_data):
    """Update states in local_countries with data from github_data."""
    # Create a lookup dictionary from GitHub data (name -> states)
    github_lookup = {}
    for country in github_data:
        country_name = country.get('name', '')
        states = country.get('states', [])
        normalized_name = normalize_country_name(country_name)
        github_lookup[normalized_name] = states
    
    # Update local countries
    updated_count = 0
    not_found_count = 0
    empty_states_count = 0
    
    for local_country in local_countries:
        country_name = local_country.get('country', '')
        normalized_name = normalize_country_name(country_name)
        
        if normalized_name in github_lookup:
            new_states = github_lookup[normalized_name]
            old_states_count = len(local_country.get('states', []))
            
            if new_states:
                local_country['states'] = new_states
                updated_count += 1
                print(f"  ✓ Updated {country_name}: {old_states_count} -> {len(new_states)} states")
            else:
                empty_states_count += 1
                print(f"  ⚠ {country_name}: GitHub data has no states (keeping existing {old_states_count} states)")
        else:
            not_found_count += 1
            print(f"  ✗ {country_name}: Not found in GitHub data (keeping existing states)")
    
    print(f"\nSummary:")
    print(f"  Updated: {updated_count} countries")
    print(f"  Not found in GitHub: {not_found_count} countries")
    print(f"  Empty states in GitHub: {empty_states_count} countries")
    
    return local_countries


def save_countries(data):
    """Save the updated countries data to the file."""
    print(f"\nSaving updated data to {LOCAL_COUNTRIES_FILE}...")
    try:
        with open(LOCAL_COUNTRIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✓ Successfully saved updated countries file")
        return True
    except Exception as e:
        print(f"✗ Error saving file: {e}")
        return False


def main():
    """Main function to orchestrate the update process."""
    print("=" * 60)
    print("Countries States Updater")
    print("=" * 60)
    print()
    
    # Check if local file exists
    if not LOCAL_COUNTRIES_FILE.exists():
        print(f"✗ Error: Local countries file not found at {LOCAL_COUNTRIES_FILE}")
        return 1
    
    # Create backup
    if not create_backup():
        print("\n⚠ Warning: Could not create backup. Continue anyway? (y/n): ", end='')
        response = input().strip().lower()
        if response != 'y':
            print("Aborted.")
            return 1
    
    # Fetch GitHub data
    github_data = fetch_github_data()
    if not github_data:
        return 1
    
    # Load local countries
    local_countries = load_local_countries()
    if not local_countries:
        return 1
    
    # Update states
    print("\nUpdating states...")
    updated_countries = update_states(local_countries, github_data)
    
    # Save updated data
    if save_countries(updated_countries):
        print("\n" + "=" * 60)
        print("✓ Update completed successfully!")
        print(f"  Backup saved at: {BACKUP_FILE}")
        print("=" * 60)
        return 0
    else:
        print("\n✗ Update failed. Backup is available at:", BACKUP_FILE)
        return 1


if __name__ == "__main__":
    exit(main())

