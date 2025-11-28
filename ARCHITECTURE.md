
# Snacklore Architecture Documentation

## Overview
Snacklore is a Flask-based web application for exploring snacks and recipes from around the world. The application uses PostgreSQL as its database and is containerized with Docker for easy deployment.

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database interactions
- **PostgreSQL**: Relational database (version 17)
- **Python**: 3.11

### Frontend
- **HTML Templates**: Jinja2 templating engine (via Flask)
- **Static Assets**: JSON data files, CSS (when added)

### Deployment
- **Docker**: Containerization
- **Fly.io**: Cloud hosting platform
- **PostgreSQL**: Embedded in container (development) or external (production)

## Application Structure

### Core Application (`app.py`)
- Flask application instance
- SQLAlchemy database connection
- Route handlers
- Database initialization on startup

### Key Components
1. **Flask App**: Main application instance with configuration
2. **Database**: SQLAlchemy ORM connected to PostgreSQL
3. **Routes**: URL routing and view functions
4. **Templates**: HTML templates in `templates/` directory
5. **Static Files**: Assets in `static/` directory

## Database Architecture

### Connection
- **URI**: `postgresql://postgres@localhost/snacklore`
- **Authentication**: Trust-based (local development)
- **Database Name**: `snacklore`
- **Auto-initialization**: Database and tables created on app startup

### Current State
- Database schema is managed through SQLAlchemy models
- Tables are created automatically via `db.create_all()` on startup

## Deployment Architecture

### Docker Container
- **Base Image**: `python:3.11-slim`
- **PostgreSQL**: Installed and configured within container
- **Port**: 5000 (exposed)
- **Startup**: `boot.sh` script handles PostgreSQL and Flask initialization

### Container Startup Process (`boot.sh`)
1. Start PostgreSQL service in background
2. Wait for PostgreSQL to be ready
3. Create database if it doesn't exist
4. Start Flask application

### Fly.io Configuration
- **Region**: Dallas (dfw)
- **Memory**: 1GB
- **CPU**: 1 shared CPU
- **Port**: 5000 (internal)
- **HTTPS**: Enforced
- **Auto-scaling**: Machines stop/start based on traffic

## File Structure

```
snacklore/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── fly.toml              # Fly.io deployment configuration
├── boot.sh               # Container startup script
├── start.sh              # Local development startup script
├── templates/
│   └── home.html         # Home page template
├── static/
│   └── countries.json    # Country data
└── wireframes/           # Design wireframes
```

## Development Workflow

### Local Development
1. Run `./start.sh` to build and start Docker container
2. Container handles PostgreSQL setup automatically
3. Flask app runs on `http://localhost:5000`

### Production Deployment
1. Application deployed to Fly.io
2. Database connection configured via environment variables
3. HTTPS enforced automatically

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (defaults to 'dev-secret-key' in development)
- `SQLALCHEMY_DATABASE_URI`: Database connection string

### Database Configuration
- SQLAlchemy tracking modifications: Disabled
- Connection pooling: Managed by SQLAlchemy
- Auto-creation: Enabled for development

## Current Routes

- `/`: Home page (renders `home.html`)

## Future Considerations

- External PostgreSQL database for production
- Environment-based configuration management
- Database migrations (Flask-Migrate)
- User authentication and authorization
- API endpoints for data access
- Frontend framework integration (if needed)
