# tests/conftest.py

import pytest
from app import create_app, db
from app.models import Todo

@pytest.fixture
def app():
    """Flask application for testing."""
    app = create_app(config_class="app.config.TestingConfig")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()

@pytest.fixture
def sample_todo(app):
    """Create a single todo for testing."""
    with app.app_context():
        todo = Todo(title='Sample Todo')
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id
    return todo_id

@pytest.fixture
def multiple_todos(app):
    """Create three todos for list testing."""
    with app.app_context():
        todo1 = Todo(title='First Todo')
        todo2 = Todo(title='Second Todo')
        todo3 = Todo(title='Third Todo')
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.add(todo3)
        db.session.commit()
        todo_ids = [todo1.id, todo2.id, todo3.id]
    return todo_ids
