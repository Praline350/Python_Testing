import pytest
import json
from unittest.mock import mock_open, patch
from tools.tools import DataBase  

CLUBS_JSON = '''{
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
}'''

COMPETITIONS_JSON = '''{
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
}'''

@pytest.fixture
def db():
    return DataBase()

def test_loadClubs(db):
    with patch('builtins.open', mock_open(read_data=CLUBS_JSON)):
        clubs = db.loadClubs()
        assert len(clubs) == 3
        assert clubs[0]['name'] == "Simply Lift"
        assert clubs[1]['email'] == "admin@irontemple.com"
        assert clubs[2]['points'] == "12"

def test_loadCompetitions(db):
    with patch('builtins.open', mock_open(read_data=COMPETITIONS_JSON)):
        competitions = db.loadCompetitions()
        assert len(competitions) == 2
        assert competitions[0]['name'] == "Spring Festival"
        assert competitions[1]['date'] == "2020-10-22 13:30:00"

