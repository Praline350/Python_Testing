import json
from datetime import datetime

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
        
    def check_competitions_status(self, competitions):
        current_time = datetime.now()
        for competition in competitions:
            competition_time = datetime.strptime(competition['date'], "%Y-%m-%d %H:%M:%S")
            competition['status'] = 'Past' if competition_time < current_time else 'Upcoming'
        self.save_competitions(competitions)
        
            
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
                print(f"Club trouvé dans la compétition: {club['name']}, Places demandées: {placesRequired}, Places actuelles: {c[club['name']]}, Points disponibles: {club['points']}")
                if c[club['name']] + placesRequired > max_places_allowed or placesRequired > int(club['points']):
                    print("Condition non remplie : dépassement de la limite autorisée ou des points du club")
                    return False
                else:
                    c[club['name']] += placesRequired
                    club_found = True
                    print(f"Places mises à jour pour le club : {c[club['name']]}")
                    return True

        if not club_found:
            print(f"Club non trouvé dans la compétition, ajout des places. Places demandées: {placesRequired}, Points disponibles: {club['points']}")
            if placesRequired <= max_places_allowed and placesRequired <= int(club['points']):
                club_registered.append({club['name']: placesRequired})
                print(f"Club ajouté avec {placesRequired} places")
                return True 
            else:
                print("Condition non remplie : dépassement de la limite autorisée ou des points du club")
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
        