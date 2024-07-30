import pytest 
import html
from flask import url_for
from server import app, find_club_by_email


@pytest.fixture
def client():
    return app.test_client()

def test_find_club_by_email():
    clubs = [
        {'email': 'admin@irontemple.com'},
        {'email': 'contact@gym.com'}
    ]

    assert find_club_by_email('admin@irontemple.com', clubs) == {'email': 'admin@irontemple.com'}
    assert find_club_by_email(' ADMIN@irontemple.com ', clubs) == {'email': 'admin@irontemple.com'}
    assert find_club_by_email('contact@gym.com', clubs) == {'email': 'contact@gym.com'}
    assert find_club_by_email('unknown@gym.com', clubs) is None
    assert find_club_by_email('', clubs) is None


class TestShowSummary:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client

    def test_index(self):
        response = self.client.get('/')
        assert response.status_code == 200

    def test_authentication_with_correct_email(self):
        correct_email = 'admin@irontemple.com'
        response = self.client.post('/showSummary', data={'email': correct_email})
        assert response.status_code == 200
        assert b'Welcome' in response.data

    def test_authentication_with_unknown_email(self):
        unknown_email = 'email@email.com'
        response = self.client.post('/showSummary', data={'email': unknown_email})
        assert response.status_code == 302
        response_follow = self.client.get(response.headers['Location'], follow_redirects=True)
        response_data = response_follow.data.decode('UTF-8')
        converted_str = html.unescape(response_data)
        assert "Email wrong" in converted_str

    def test_authentication_with_empty_email(self):
        empty_email = ''
        response = self.client.post('/showSummary', data={'email': empty_email})
        assert response.status_code == 302
        response_follow = self.client.get(response.headers['Location'], follow_redirects=True)
        response_data = response_follow.data.decode('UTF-8')
        converted_str = html.unescape(response_data)
        assert "Email wrong" in converted_str

    def test_authentication_with_maj(self):
        email = 'ADMIN@irontemple.cOm'
        response = self.client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert b'Welcome' in response.data

    def test_authentication_with_space(self):
        email = 'admin@irontemple.com '
        response = self.client.post('/showSummary', data={'email': email})
        assert response.status_code == 200