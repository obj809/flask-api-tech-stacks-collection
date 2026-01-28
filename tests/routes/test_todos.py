# tests/routes/test_todos.py

from app.models import Todo


# Happy Path Tests - List Todos

def test_list_todos_empty(client):
    """Test listing todos when database is empty."""
    response = client.get('/api/todos/')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_list_todos_with_data(client, app):
    """Test listing todos when database has data."""
    # Create test todos directly in database
    with app.app_context():
        todo1 = Todo(title='First Todo')
        todo2 = Todo(title='Second Todo')
        from app import db
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.commit()

    response = client.get('/api/todos/')

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['title'] == 'First Todo'
    assert data[1]['title'] == 'Second Todo'


# Happy Path Tests - Create Todo

def test_create_todo_success(client):
    """Test creating a new todo with valid data."""
    response = client.post('/api/todos/',
                          json={'title': 'Test Todo'},
                          content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Todo'
    assert 'id' in data
    assert isinstance(data['id'], int)


def test_create_todo_persists_to_database(client, app):
    """Test that created todo is saved to database."""
    response = client.post('/api/todos/',
                          json={'title': 'Persistent Todo'},
                          content_type='application/json')

    todo_id = response.get_json()['id']

    with app.app_context():
        todo = Todo.query.get(todo_id)
        assert todo is not None
        assert todo.title == 'Persistent Todo'


def test_create_todo_with_trailing_slash(client):
    """Test creating todo works with trailing slash."""
    response = client.post('/api/todos/',
                          json={'title': 'Trailing Slash Todo'},
                          content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Trailing Slash Todo'


# Happy Path Tests - Get Single Todo

def test_get_todo_success(client, app):
    """Test getting a single todo by ID."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Get Me')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.get(f'/api/todos/{todo_id}')

    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == todo_id
    assert data['title'] == 'Get Me'


def test_get_todo_with_trailing_slash(client, app):
    """Test getting todo works with trailing slash."""
    with app.app_context():
        todo = Todo(title='Get Me With Slash')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.get(f'/api/todos/{todo_id}/')

    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Get Me With Slash'


# Happy Path Tests - Update Todo

def test_update_todo_success(client, app):
    """Test updating a todo with valid data."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Original Title')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.put(f'/api/todos/{todo_id}',
                         json={'title': 'Updated Title'},
                         content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == todo_id
    assert data['title'] == 'Updated Title'


def test_update_todo_persists_to_database(client, app):
    """Test that updated todo is saved to database."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Before Update')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    client.put(f'/api/todos/{todo_id}',
              json={'title': 'After Update'},
              content_type='application/json')

    # Verify in database
    with app.app_context():
        todo = Todo.query.get(todo_id)
        assert todo.title == 'After Update'


def test_update_todo_with_trailing_slash(client, app):
    """Test updating todo works with trailing slash."""
    with app.app_context():
        todo = Todo(title='Original')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.put(f'/api/todos/{todo_id}/',
                         json={'title': 'Updated'},
                         content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated'


# Happy Path Tests - Delete Todo

def test_delete_todo_success(client, app):
    """Test deleting a todo."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Delete Me')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.delete(f'/api/todos/{todo_id}')

    assert response.status_code == 204
    assert response.data == b''


def test_delete_todo_removes_from_database(client, app):
    """Test that deleted todo is removed from database."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Delete Me Forever')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    client.delete(f'/api/todos/{todo_id}')

    # Verify it's gone from database
    with app.app_context():
        todo = Todo.query.get(todo_id)
        assert todo is None


def test_delete_todo_with_trailing_slash(client, app):
    """Test deleting todo works with trailing slash."""
    with app.app_context():
        todo = Todo(title='Delete With Slash')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.delete(f'/api/todos/{todo_id}/')

    assert response.status_code == 204


# Error Cases - Create Todo

def test_create_todo_missing_title(client):
    """Test creating todo without title returns 400."""
    response = client.post('/api/todos/',
                          json={},
                          content_type='application/json')

    assert response.status_code == 400
    data = response.get_json()
    assert 'Title is required' in data.get('message', '')


def test_create_todo_empty_json(client):
    """Test creating todo with empty JSON returns 400."""
    response = client.post('/api/todos/',
                          json={},
                          content_type='application/json')

    assert response.status_code == 400


def test_create_todo_no_body(client):
    """Test creating todo without request body returns 400."""
    response = client.post('/api/todos/',
                          content_type='application/json')

    assert response.status_code == 400


# Error Cases - Get Todo

def test_get_todo_not_found(client):
    """Test getting non-existent todo returns 404."""
    response = client.get('/api/todos/99999')

    assert response.status_code == 404
    data = response.get_json()
    assert 'not found' in data.get('message', '').lower()


def test_get_todo_invalid_id(client):
    """Test getting todo with invalid ID returns 404."""
    response = client.get('/api/todos/invalid')

    assert response.status_code == 404


# Error Cases - Update Todo

def test_update_todo_not_found(client):
    """Test updating non-existent todo returns 404."""
    response = client.put('/api/todos/99999',
                         json={'title': 'Updated'},
                         content_type='application/json')

    assert response.status_code == 404
    data = response.get_json()
    assert 'not found' in data.get('message', '').lower()


def test_update_todo_missing_title(client, app):
    """Test updating todo without title returns 400."""
    # Create a todo
    with app.app_context():
        todo = Todo(title='Original')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.put(f'/api/todos/{todo_id}',
                         json={},
                         content_type='application/json')

    assert response.status_code == 400
    data = response.get_json()
    assert 'Title is required' in data.get('message', '')


def test_update_todo_empty_json(client, app):
    """Test updating todo with empty JSON returns 400."""
    with app.app_context():
        todo = Todo(title='Original')
        from app import db
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    response = client.put(f'/api/todos/{todo_id}',
                         json={},
                         content_type='application/json')

    assert response.status_code == 400


# Error Cases - Delete Todo

def test_delete_todo_not_found(client):
    """Test deleting non-existent todo returns 404."""
    response = client.delete('/api/todos/99999')

    assert response.status_code == 404
    data = response.get_json()
    assert 'not found' in data.get('message', '').lower()


# Edge Cases

def test_create_todo_with_long_title(client):
    """Test creating todo with 255 character title."""
    long_title = 'A' * 255
    response = client.post('/api/todos/',
                          json={'title': long_title},
                          content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == long_title


def test_create_todo_with_unicode(client):
    """Test creating todo with unicode characters."""
    unicode_title = 'Todo with emoji 🎉 and unicode: 你好世界'
    response = client.post('/api/todos/',
                          json={'title': unicode_title},
                          content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == unicode_title


def test_create_todo_with_special_characters(client):
    """Test creating todo with special characters."""
    special_title = 'Special chars: !@#$%^&*()_+-={}[]|:;"<>,.?/'
    response = client.post('/api/todos/',
                          json={'title': special_title},
                          content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == special_title


def test_create_multiple_todos(client):
    """Test creating multiple todos."""
    titles = ['First', 'Second', 'Third']

    for title in titles:
        response = client.post('/api/todos/',
                              json={'title': title},
                              content_type='application/json')
        assert response.status_code == 201

    # Verify all were created
    response = client.get('/api/todos/')
    data = response.get_json()
    assert len(data) == 3
