import pytest
from tools.tools import Utils




def test_find_club_by_email():
    utils = Utils()
    clubs = [
        {'email': 'admin@irontemple.com'},
        {'email': 'contact@gym.com'}
    ]

    assert utils.find_club_by_email('admin@irontemple.com', clubs) == {'email': 'admin@irontemple.com'}
    assert utils.find_club_by_email(' ADMIN@irontemple.com ', clubs) == {'email': 'admin@irontemple.com'}
    assert utils.find_club_by_email('contact@gym.com', clubs) == {'email': 'contact@gym.com'}
    assert utils.find_club_by_email('unknown@gym.com', clubs) is None
    assert utils.find_club_by_email('', clubs) is None
    
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
        result = self.utils.point_ajustement(self.club, self.competition, placesRequired)
        assert result == 'Not enough points for booking'

    def test_not_enough_places(self):
        placesRequired = 3
        self.competition['numberOfPlaces'] = 2
        result = self.utils.point_ajustement(self.club, self.competition, placesRequired)
        assert result == 'Not enough places available in the competition'

    def test_succes_adjustement(self):
        placesRequired = 3
        result = self.utils.point_ajustement(self.club, self.competition, placesRequired)
        assert result == 'Great-booking complete!'
        assert self.club['points'] == 1
        assert self.competition['numberOfPlaces'] == 7


class TestUtils:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.utils = Utils()
        self.club = {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        }
        self.club2 = {   
            "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        }
        self.club3 = {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        }
        self.competition = {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            "clubsRegistered" : []
        }


    def test_club_add_club_registered(self):
        validate = self.utils.club_add_places(self.club, self.competition, 5)
        assert validate == True
        assert self.competition['clubsRegistered'][0] == {self.club['name']: 5}

    def test_add_existing_club(self):
        validate = self.utils.club_add_places(self.club, self.competition, 5)
        assert self.competition['clubsRegistered'][0] == {self.club['name']: 5}
        assert validate == True
        validate = self.utils.club_add_places(self.club, self.competition, 5)
        assert validate == True
        assert self.competition['clubsRegistered'] == [{self.club['name']: 10}]

    def test_add_multi_clubs(self):
        validate = self.utils.club_add_places(self.club, self.competition, 5)
        validate2 = self.utils.club_add_places(self.club2, self.competition, 5)
        assert validate and validate2 == True
        assert self.competition['clubsRegistered'] == [{self.club['name']: 5},{self.club2['name']: 5}]

    def test_add_too_much_places(self):
        validate = self.utils.club_add_places(self.club, self.competition, 13)
        assert validate == False
        self.utils.club_add_places(self.club, self.competition, 12)
        assert self.competition['clubsRegistered'] == [{self.club['name']: 12}]
        
    def test_add_places_exceeding_points(self):
        # Demande plus de places que le club n'a de points (14 > 13)
        validate = self.utils.club_add_places(self.club3, self.competition, 5)
        assert validate == False
        # Vérifie que le club n'est pas ajouté à clubsRegistered
        assert len(self.competition['clubsRegistered']) == 0


