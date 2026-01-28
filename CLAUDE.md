# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Flask REST API application for Todo management with MySQL database backend. Uses Flask-RESTx for API documentation (Swagger UI), Flask-SQLAlchemy for database ORM, and Flask-Migrate/Alembic for database migrations.

## Development Commands

### Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run Application
```bash
python3 run.py
```
Server runs on `http://0.0.0.0:5001`

### API Documentation
Access Swagger UI at: `http://localhost:5001/api/docs`

### Testing
```bash
pytest                                      # Run all tests
pytest tests/routes                         # Run route tests
pytest tests/routes/test_todos.py          # Run specific test file
pytest --cov=app tests/                    # Run with coverage
pytest --cov=app --cov-report=html tests/  # Generate HTML coverage report
```

### Database Migrations
```bash
flask db upgrade         # Apply migrations
flask db history        # View migration history
flask db stamp head     # Mark database as current
```

### Utility Scripts
Located in `scripts/` directory:
- `test_env_vars.py` - Verify environment variables are loaded
- `db_connection_check.py` - Test database connectivity
- `db_data_collection_and_export.py` - Export database data
- `manual_endpoint_test.py` - Manual API endpoint testing

## Architecture

### Application Factory Pattern
Uses factory pattern in `app/__init__.py` via `create_app()`. This enables:
- Multiple app instances with different configurations
- Proper testing with `TestingConfig` (in-memory SQLite)
- Clean separation of concerns

### Configuration System
- `app/config.py` contains `Config` class for production and `TestingConfig` for tests
- Production requires `SQLALCHEMY_DATABASE_URI` in `.env` file (MySQL connection string)
- Testing automatically uses in-memory SQLite database
- Environment variables loaded via `python-dotenv` in `run.py` before app creation

### Database Layer
- **ORM**: Flask-SQLAlchemy with models in `app/models.py`
- **Migrations**: Flask-Migrate/Alembic in `migrations/` directory
- **Database**: MySQL/MariaDB for production, SQLite for testing
- **Connection String Format**: `mysql+pymysql://USER:PASSWORD@HOST:PORT/DB_NAME`

### API Structure
- **Framework**: Flask-RESTx for automatic Swagger/OpenAPI documentation
- **Namespace Pattern**: Each route module exports a Namespace (not Blueprint)
  - `app/routes/main.py` → mounted at `/api` (health check)
  - `app/routes/helloworld.py` → mounted at `/api/helloworld`
  - `app/routes/todos.py` → mounted at `/api/todos` (full CRUD)
- **Models**: Flask-RESTx models defined in route files for request/response validation
- **Registration**: Namespaces registered via `api.add_namespace()` in `create_app()`

### Route Implementation Pattern
Routes use Flask-RESTx Resource classes:
```python
@namespace.route('/<int:id>')
@namespace.param('id', 'The identifier')
class ResourceName(Resource):
    @namespace.doc('operation_name')
    @namespace.marshal_with(model)
    def get(self, id):
        # Implementation
```

Key decorators:
- `@namespace.doc()` - Swagger documentation
- `@namespace.marshal_with()` - Response serialization
- `@namespace.expect()` - Request body validation
- `@namespace.abort()` - Error responses

### Testing Infrastructure
- **Framework**: pytest with fixtures in `tests/conftest.py`
- **Fixtures**: `app` fixture creates test app with `TestingConfig`, `client` fixture provides test client
- **Database**: Automatically creates/destroys in-memory database per test session
- **Pattern**: Use `client.get()`, `client.post()`, etc. for API testing

## Key Implementation Notes

### Adding New Routes
1. Create namespace in `app/routes/new_route.py`
2. Define Flask-RESTx models for request/response schemas
3. Create Resource classes with HTTP methods
4. Import and register namespace in `app/__init__.py` via `api.add_namespace()`

### Database Model Changes
1. Modify models in `app/models.py`
2. Import new models in `app/__init__.py` before `migrate.init_app()`
3. Generate migration: `flask db migrate -m "description"`
4. Review generated migration in `migrations/versions/`
5. Apply: `flask db upgrade`

### Environment Variables
Required in `.env`:
- `SQLALCHEMY_DATABASE_URI` - MySQL connection string (validated on startup)
- `SECRET_KEY` - Flask secret key
- `DEBUG` - Set to 'True' or 'False'

Use `.env.example` as template.

### CORS
Flask-CORS enabled globally for all origins in `create_app()`. Modify in `app/__init__.py` if restrictions needed.

### Current Branch Context
Currently on `supabase-integration` branch - integration work in progress with Supabase (PostgreSQL-based backend).
