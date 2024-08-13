import pytest
import json
from unittest.mock import mock_open, patch
from tools.tools import DataBase


CLUBS_JSON = {
    "clubs":[
        {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        },
        {
            "name":"Iron Temple",
            "email": "admin@irontemple.com",
            "points":"4"
        },
        {
            "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        }
    ]
}

COMPETITIONS_JSON = {
    "competitions": [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
}

class TestDataBase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_base = DataBase()
         

    def test_load_clubs(self):
        clubs = self.data_base.load_clubs()
        assert len(clubs) == 3
        assert clubs[0]['name'] == "Simply Lift"
        assert clubs[1]['email'] == "admin@irontemple.com"
        assert clubs[2]['points'] == "12"

    def test_load_competitions(self):
        competitions = self.data_base.load_competitions()
        assert len(competitions) == 3
        assert competitions[0]['name'] == "Spring Festival"
        assert competitions[1]['date'] == "2020-10-22 13:30:00"

    def test_update_club_points(self):
        self.data_base.update_club_points("Simply Lift", 13)
        clubs = self.data_base.load_clubs()
        assert clubs[0]['name'] == "Simply Lift"
        assert clubs[0]['points'] == "13"
