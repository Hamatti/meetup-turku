from flask import Flask, render_template
from models import Meetup
import meetupdirectory

app = Flask(__name__)

@app.route('/')
def hello():
    meetups = []
    for meetup in meetupdirectory.meetups:
        mt = Meetup(meetup)
        mt.get_events()
        meetups.append(mt)
    return render_template('index.html', meetups=meetups)

app.run()
