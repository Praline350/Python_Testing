import json
import os
from dotenv import load_dotenv
from flask import Flask,render_template,request,redirect,flash,url_for
from tools import DataBase, Utils

load_dotenv()


data_base = DataBase()
utils = Utils()

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = data_base.loadCompetitions()
clubs = data_base.loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    competitions = data_base.loadCompetitions()
    clubs = data_base.loadClubs()
    email = request.form['email']
    selected_club = utils.find_club_by_email(email, clubs)
    if selected_club is None:
        flash("Email wrong")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=selected_club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    message = utils.point_ajustement(club, competition, placesRequired)
    flash(message)
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))