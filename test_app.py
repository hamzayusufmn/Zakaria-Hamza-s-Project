import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF just during test
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'Med Delights' in res.data

def test_menu_page_displays(client):
    res = client.get('/menu/', follow_redirects=True)  # fix 308 redirect
    assert res.status_code == 200
    assert b'Appetizers' in res.data or b'Shawarma' in res.data

def test_feedback_form_submission(client):
    res = client.post('/feedback', data={
        'name': 'Bot 1',
        'email': 'test@capstone.com',
        'phone': '123-456-7890',
        'rating': '5',
        'visited_on': '2024-05-10',
        'message': 'Fire food.'
    }, follow_redirects=True)

    assert res.status_code == 200
    assert b'Thank You for Your Feedback' in res.data
