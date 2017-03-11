from flask import Flask, render_template
from models import Meetup
import meetupdirectory
import os, json

app = Flask(__name__)
app.use_reloader=False
app.debug=True


@app.route('/')
def hello():
    data = json.load(open('next_events.json'))
    updated = data['updated']
    meetups = data['data']
    return render_template('index.html', meetups=meetups, updated=updated)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 37412))
    app.run(host='0.0.0.0', port=port)
