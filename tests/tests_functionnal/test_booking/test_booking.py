import pytest 
from unittest.mock import patch
import html
from flask import url_for
from server import Server
from tools.tools import Utils


@pytest.fixture(scope="class")
def client():
    server = Server()
    return server.app.test_client()


class TestBooking:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.clubA = {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
        self.competitionA = {
            "name": "Spring Festival",
            "date": "2025-03-27 10:00:00",
            "numberOfPlaces": "25",
            "status": True,
            "clubsRegistered": []
        }
    
    def test_purchase_places_success(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': 'Spring Festival',
            'places': '5'
        })
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data

    def test_purchase_places_not_enough_points(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'Iron Temple',
            'competition': 'Spring Festival',
            'places': '10'
        })
        assert response.status_code == 200
        assert b'Exceeding the authorized limit or club points' in response.data

    def test_purchase_places_not_enough_places(self):
        response = self.client.post('/purchasePlaces', data={
            'club': 'She Lifts',
            'competition': 'Testing',
            'places': '2'
        })
        assert response.status_code == 200
        assert b'Not enough places available in the competition' in response.data

    def test_book_valid_club_and_competiton(self):
        response = self.client.get(f"/book/{self.competitionA['name']}/{self.clubA['name']}")
        assert response.status_code == 200
        assert b'Booking for' in response.data

    def test_book_invalid_club(self):
        response = self.client.get(f"book/{self.competitionA['name']}/invalidclub")
        assert response.status_code == 302
        
    def test_book_invalid_competition(self):
        response = self.client.get(f"book/invalidcompetition/{self.clubA['name']}")
        assert response.status_code == 302
        