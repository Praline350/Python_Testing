import pytest 
from unittest.mock import patch
import html
from flask import url_for
from server import app
from tools.tools import Utils


@pytest.fixture
def client():
    return app.test_client()


class TestBooking:
    def test_purchase_places_success(self, client):
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': 'Spring Festival',
            'places': '5'
        })
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data

    def test_purchase_places_not_enough_points(self, client):
        response = client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '10'
        })
        assert response.status_code == 200
        assert b'Not enough points for booking' in response.data

    def test_purchase_places_not_enough_places(self, client):
        response = client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': 'Testing',
            'places': '2'
        })
        assert response.status_code == 200
        assert b'Not enough places available in the competition' in response.data

