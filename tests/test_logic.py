import pytest

from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


@pytest.mark.parametrize("path, expected_headers", [
    ("/", {"content-type": "text/html; charset=utf-8"}),
    ("/services/", {"content-type": "text/html; charset=utf-8"}),
    ("/representatives", {"content-type": "text/html; charset=utf-8"}),
    ("/about/", {"content-type": "text/html; charset=utf-8"}),
    ("/contact/", {"content-type": "text/html; charset=utf-8"}),
])
def test_verify_headers(path, expected_headers):
    response = client.get(path)

    assert response.status_code == 200
    assert response.request.method == 'GET'
    for header_name, expected_value in expected_headers.items():
        assert header_name in response.headers
        assert response.headers[header_name].lower() == expected_value.lower()


def test_post_contact():
    response = client.post('/contact', data={
        'name': 'Andrew',
        'email': 'any@gmail.com',
        'phone': '0123456789',
        'message': 'Anything in here'
    })
    assert response.status_code == 200
    assert response.request.method == 'POST'
    assert 'Thank you for your submission!' in response.text


def test_post_contact_failed():
    response = client.post('/contact', data={
        'name': '01234',
        'email': 'anygmail.com',
        'phone': 'asdas',
        'message': 'Anything in here'
    })

    assert response.status_code == 422
    assert response.request.method == 'POST'

