import json

CLUB_PATH = 'clubs.json'
COMPETITION_PATH = 'competitions.json'

class DataBase:
    def __init__(self):
        self.club_db = CLUB_PATH
        self.competition_db = COMPETITION_PATH


    def load_clubs(self):
        with open(self.club_db) as clubs:
            listOfClubs = json.load(clubs)['clubs']
            return listOfClubs
        
    def load_competitions(self):
        with open(self.competition_db, 'r') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
        
    def save_clubs(self, clubs):
        with open(self.club_db, 'w') as file:
            json.dump({"clubs": clubs}, file, indent=4)

    def save_competitions(self, competitions):
        with open(self.competition_db, 'w') as file:
            json.dump({"competitions": competitions}, file, indent=4)

    def update_club_points(self, club_name, new_points):
        clubs = self.load_clubs()
        for club in clubs:
            if club['name'] == club_name:
                club['points'] = str(new_points)  # Convertir les points en chaîne de caractères
                break
        self.save_clubs(clubs)
        
        
            


        

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
        