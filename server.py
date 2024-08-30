import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, flash, url_for
from tools.tools import Utils, DataBase

load_dotenv()

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'something_special'
        self.data_base = DataBase()
        self.utils = Utils()
        self.competitions = self.data_base.load_competitions()
        self.data_base.check_competitions_status(self.competitions)
        self.clubs = self.data_base.load_clubs()

        # Configuration des routes
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/showSummary', 'showSummary', self.showSummary, methods=['POST'])
        self.app.add_url_rule('/book/<competition>/<club>', 'book', self.book)
        self.app.add_url_rule('/purchasePlaces', 'purchasePlaces', self.purchasePlaces, methods=['POST'])
        self.app.add_url_rule('/PointsBoard', 'pointsBoard', self.pointsBoard, methods=['GET'])
        self.app.add_url_rule('/logout', 'logout', self.logout)


    def index(self):
        return render_template('index.html')

    def showSummary(self):
        email = request.form['email']
        selected_club = self.utils.find_club_by_email(email, self.clubs)
        if selected_club is None:
            flash("Email wrong")
            return redirect(url_for('index'))
        return render_template('welcome.html', club=selected_club, competitions=self.competitions)

    def book(self, competition, club):
        foundClub = [c for c in self.clubs if c['name'] == club]
        foundCompetition = [c for c in self.competitions if c['name'] == competition]
        

        if not foundClub:
            flash(f"Club '{club}' not found. Please select a valid club.")
            return redirect(url_for('index'))  # Redirige vers une page appropriée

        if not foundCompetition:
            flash(f"Competition '{competition}' not found. Please select a valid competition.")
            return redirect(url_for('index'))  # Redirige vers une page appropriée
        
        # Calcul du nombre maximum de places qu'un club peux reserver pour validation Front
        max_places = min(12, int(foundClub[0]['points']), int(foundCompetition[0]['numberOfPlaces']))

        return render_template('booking.html', club=foundClub[0], competition=foundCompetition[0], max_places=max_places)

    def purchasePlaces(self):
        competition = [c for c in self.competitions if c['name'] == request.form['competition']][0]
        club = [c for c in self.clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        validation = self.utils.club_add_places(club, competition, placesRequired)
        if not validation:
            flash("Exceeding the authorized limit or club points")
        else:
            message = self.utils.point_ajustement(club, competition, placesRequired)
            flash(message)
        return render_template('welcome.html', club=club, competitions=self.competitions)

    def pointsBoard(self):
        return render_template('board.html', clubs=self.clubs, competitions=self.competitions)

    def logout(self):
        return redirect(url_for('index'))

    def run(self, host='0.0.0.0', port=5000, debug=True):
        self.app.run(host=host, port=port, debug=debug)



if __name__ == '__main__':
    server = Server()
    server.run()