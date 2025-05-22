from flask import Flask, render_template, session, redirect, url_for
from random import randint

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-random-key'

# Initialize game state
def init_game():
    session['current'] = randint(1, 100)
    session['score'] = 0
    session['message'] = ''
    session['game_over'] = False
