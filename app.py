from flask import Flask, render_template
from models import Meetup
import meetupdirectory
import os

app = Flask(__name__)
app.use_reloader=False
app.debug=False


@app.route('/')
def hello():
    meetups = []
    for meetup in meetupdirectory.meetups:
        mt = Meetup(meetup)
        mt.get_events()
        meetups.append(mt)
    return render_template('index.html', meetups=meetups)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 37412))
    app.run(host='0.0.0.0', port=port)
