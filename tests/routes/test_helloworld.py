# tests/routes/test_helloworld.py

def test_helloworld_success(client):
    """Test hello world endpoint returns success."""
    response = client.get('/api/helloworld/')

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['message'] == 'Hello, World!'


def test_helloworld_with_trailing_slash(client):
    """Test hello world endpoint works with trailing slash."""
    response = client.get('/api/helloworld/')

    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Hello, World!'


def test_helloworld_response_structure(client):
    """Test hello world response has all required fields."""
    response = client.get('/api/helloworld/')

    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert 'message' in data


def test_helloworld_content_type(client):
    """Test hello world endpoint returns JSON content type."""
    response = client.get('/api/helloworld/')

    assert response.status_code == 200
    assert response.content_type == 'application/json'
