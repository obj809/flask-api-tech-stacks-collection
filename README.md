# Flask API Tech Stacks Collection

[![Tests](https://github.com/obj809/flask-api-tech-stacks-collection/actions/workflows/tests.yml/badge.svg)](https://github.com/obj809/flask-api-tech-stacks-collection/actions/workflows/tests.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)](https://github.com/obj809/flask-api-tech-stacks-collection)

A Flask REST API application for Todo management with MySQL database backend, comprehensive test coverage, and CI/CD integration.

## Features

- RESTful API with full CRUD operations
- Flask-RESTx for automatic Swagger/OpenAPI documentation
- Flask-SQLAlchemy ORM with database migrations
- Comprehensive test suite (34 tests, 96% coverage)
- GitHub Actions CI/CD pipeline
- Clean, developer-friendly pytest configuration

![Swagger Documentation](screenshots/documentation-light.png)

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/obj809/flask-api-tech-stacks-collection.git
cd flask-api-tech-stacks-collection

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Application

```bash
python3 run.py
```

Server runs on `http://0.0.0.0:5001`

### API Documentation

Access Swagger UI at: `http://localhost:5001/api/docs`

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/routes/test_todos.py

# Run with coverage
pytest --cov=app tests/

# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/
```

### Test Coverage

- **34 tests** covering all API endpoints
- **96% overall coverage**
- 100% coverage on all route handlers
- Tests for happy paths, error cases, and edge cases

## API Endpoints

### Health Check
- `GET /api/` - Health check endpoint

### Hello World
- `GET /api/helloworld/` - Simple greeting endpoint

### Todos
- `GET /api/todos/` - List all todos
- `POST /api/todos/` - Create a new todo
- `GET /api/todos/<id>` - Get a specific todo
- `PUT /api/todos/<id>` - Update a todo
- `DELETE /api/todos/<id>` - Delete a todo

## CI/CD

The project uses GitHub Actions for continuous integration:
- Runs tests on Python 3.10, 3.11, and 3.12
- Executes on every push and pull request
- Generates coverage reports
- See `.github/workflows/tests.yml` for configuration

## Project Structure

```
flask-api-tech-stacks-collection/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration classes
│   ├── models.py            # SQLAlchemy models
│   └── routes/              # API route modules
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── routes/              # Route tests
├── migrations/              # Alembic database migrations
├── .github/workflows/       # CI/CD configuration
├── pytest.ini               # Pytest configuration
└── requirements.txt         # Python dependencies
```

## Development

See [CLAUDE.md](CLAUDE.md) for detailed development guidelines and commands.

## License

MIT License


