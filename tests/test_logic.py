import pytest
from fastapi.testclient import TestClient
import main

# Create a FastAPI TestClient instance
client = TestClient(main.app)


# Define a parameterized test to verify headers for various paths
@pytest.mark.parametrize("path, expected_headers", [
    ("/", {"content-type": "text/html; charset=utf-8"}),
    ("/services/", {"content-type": "text/html; charset=utf-8"}),
    ("/representatives", {"content-type": "text/html; charset=utf-8"}),
    ("/about/", {"content-type": "text/html; charset=utf-8"}),
    ("/contact/", {"content-type": "text/html; charset=utf-8"}),
])
def test_verify_headers(path, expected_headers):
    """
    Test to verify the headers for different paths.

    Args:
        path (str): Path to test.
        expected_headers (dict): Expected headers for the path.

    Returns:
        None
    """
    response = client.get(path)

    assert response.status_code == 200
    assert response.request.method == 'GET'
    for header_name, expected_value in expected_headers.items():
        assert header_name in response.headers
        assert response.headers[header_name].lower() == expected_value.lower()


# Define a test for successful form submission
def test_post_contact():
    """
    Test the successful submission of the contact form.

    Returns:
        None
    """
    response = client.post('/contact', data={
        'name': 'Andrew',
        'email': 'any@gmail.com',
        'phone': '0123456789',
        'message': 'Anything in here'
    })

    assert response.status_code == 200
    assert response.request.method == 'POST'
    assert 'Thank you for your submission!' in response.text


# Define a test for failed form submission
def test_post_contact_failed():
    """
    Test the failed submission of the contact form.

    Returns:
        None
    """
    response = client.post('/contact', data={
        'name': '01234',
        'email': 'anygmail.com',
        'phone': 'asdas',
        'message': 'Anything in here'
    })

    assert response.status_code == 422
    assert response.request.method == 'POST'

