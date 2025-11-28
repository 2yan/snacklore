#!/bin/bash
set -e

# Start PostgreSQL in the background as postgres user
su - postgres -c "/usr/lib/postgresql/17/bin/postgres -D /var/lib/postgresql/17/main -c config_file=/etc/postgresql/17/main/postgresql.conf" &

# Wait for PostgreSQL to be ready
until su - postgres -c "psql -c '\q'" 2>/dev/null; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

# Create database if it doesn't exist
su - postgres -c "psql -c \"SELECT 1 FROM pg_database WHERE datname = 'snacklore'\"" | grep -q 1 || su - postgres -c "psql -c 'CREATE DATABASE snacklore;'"

# Initialize database schema
echo "Initializing database schema..."
su - postgres -c "psql -d snacklore -f /app/boot/init_db.sql" || {
  echo "Warning: Database schema initialization may have failed or tables already exist"
}

# Seed countries and states
echo "Seeding countries and states..."
cd /app && python3 boot/seed_data.py

# Seed recipes
echo "Seeding recipes..."
cd /app && python3 boot/seed_recipes.py

# Keep PostgreSQL running and start Flask
exec python app.py

