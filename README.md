# Snacklore - Fresh Start

This is a minimal setup for the Snacklore project.

## Contents

- **app.py**: Minimal Flask application with Hello World.
- **boot.sh**: Internal script to start PostgreSQL and the Flask app inside the container.
- **start.sh**: Host script to build and run the Docker container.
- **Dockerfile**: Configuration to build the container.
- **static/countries.json**: Country data.

## Running

Simply run the start script:

```bash
./start.sh
```

Or manually:

```bash
docker build -t snacklore .
docker run -p 5000:5000 snacklore
```
