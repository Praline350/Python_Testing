import json
from flask import flash

CLUB_PATH = 'clubs.json'
COMPETITION_PATH = 'competitions.json'

class DataBase:
    def __init__(self):
        self.club_db = CLUB_PATH
        self.competition_db = COMPETITION_PATH


    def loadClubs(self):
        with open(self.club_db) as clubs:
            listOfClubs = json.load(clubs)['clubs']
            return listOfClubs


    def loadCompetitions(self):
        with open(self.competition_db) as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
        
    def write(self, path, data):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)


        

class Utils:
    def __init__(self):
        pass
    
    def find_club_by_email(self, email, clubs):
        email = email.lower().strip()
        for club in clubs:
            if club['email'] == email:
                return club
        return None
    
    def club_add_places(self, club, competition, placesRequired):
        club_registered = competition['clubsRegistered']
        club_found = False
        max_places_allowed = 12

        for c in club_registered:
            if club['name'] in c:
                if c[club['name']] + placesRequired > max_places_allowed:
                    return False
                else: 
                    c[club['name']] += placesRequired
                    club_found = True
                    return True

        if not club_found:
            if placesRequired <= max_places_allowed:
                club_registered.append({club['name']: placesRequired})
                return True 
            else:
                return False

    def point_ajustement(self, club, competition, placesRequired):
        if placesRequired > int(club['points']):
            return 'Not enough points for booking'
        elif placesRequired > int(competition['numberOfPlaces']):
            return'Not enough places available in the competition'
        else:
            # Deduct points and update the number of places
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired
            return 'Great-booking complete!'