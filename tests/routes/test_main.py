# tests/routes/test_main.py

def test_health_check_success(client):
    """Test health check endpoint returns success."""
    response = client.get('/api/')

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == 'Todo Management API is running'
    assert data['version'] == '1.0'


def test_health_check_with_trailing_slash(client):
    """Test health check endpoint works with trailing slash."""
    response = client.get('/api/')

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'


def test_health_check_response_structure(client):
    """Test health check response has all required fields."""
    response = client.get('/api/')

    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'message' in data
    assert 'version' in data


def test_health_check_content_type(client):
    """Test health check endpoint returns JSON content type."""
    response = client.get('/api/')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
