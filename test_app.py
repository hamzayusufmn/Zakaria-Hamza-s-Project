# test_routes.py

import pytest
from app import app

# sets up a test client for making requests like a browser would
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    """
    Makes sure the home page loads with a 200 status code.
    Also checks if 'Med Delights' is somewhere in the HTML.
    If this fails, maybe the route is broken or the page isn’t showing the name.
    """
    res = client.get('/')
    assert res.status_code == 200
    assert b'Med Delights' in res.data

def test_menu_page_displays(client):
    """
    Checks if the /menu page loads.
    Looks for either 'Appetizers' or a sample food name like 'Shawarma'.
    If this fails, menu route or data might be missing.
    """
    res = client.get('/menu')
    assert res.status_code == 200
    assert b'Appetizers' in res.data or b'Shawarma' in res.data

def test_feedback_form_submission(client):
    """
    This one submits fake feedback using POST.
    It should redirect to the confirmation page and show the thank you message.
    If this breaks, maybe the form or redirect isn’t wired up right.
    """
    res = client.post('/feedback', data={
        'name': 'Test Guy',
        'email': 'test@capstone.com',
        'message': 'Fire food.'
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b'Thank You for Your Feedback' in res.data
