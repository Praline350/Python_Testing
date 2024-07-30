import pytest 
from unittest.mock import patch
import html
from flask import url_for
from server import app
from tools import Utils


@pytest.fixture
def client():
    return app.test_client()

class TestPointAdjustement:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.utils = Utils()
        self.club = {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
        }
        self.competition = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "10"
        }
        
    def test_not_enough_points(self):
        placesRequired = 6
        with patch('tools.flash') as mock_flash:
            self.utils.point_ajustement(self.club, self.competition, placesRequired)
            mock_flash.assert_called_once_with('Not enough points for booking')

    def test_not_enough_places(self):
        placesRequired = 3
        self.competition['numberOfPlaces'] = 2
        with patch('tools.flash') as mock_flash:
            self.utils.point_ajustement(self.club, self.competition, placesRequired)
            mock_flash.assert_called_once_with('Not enough places available in the competition')

    def test_succes_adjustement(self):
        placesRequired = 3
        with patch('tools.flash') as mock_flash:
            self.utils.point_ajustement(self.club, self.competition, placesRequired)
            mock_flash.assert_called_once_with('Great-booking complete!')
            assert self.club['points'] == 1
            assert self.competition['numberOfPlaces'] == 7

class TestBooking:
    

    def test_purchase_places_success(self, client):
        response = client.post('/purchasePlaces', data={
            'club': 'Simply Lift',
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
            'club': 'Simply Lift',
            'competition': 'Testing',
            'places': '2'
        })
        assert response.status_code == 200
        print(response.data)
        assert b'Not enough places available in the competition' in response.data