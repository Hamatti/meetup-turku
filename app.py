from flask import Flask, render_template
from models import Meetup

from datetime import datetime
import os, json
import psycopg2, psycopg2.extras
import urlparse

app = Flask(__name__)
app.use_reloader=False
app.debug=True

urlparse.uses_netloc.append('postgres')
db_url = urlparse.urlparse(os.environ.get('DATABASE_URL'))

conn = psycopg2.connect(
            database=db_url.path[1:],
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port
    )


@app.route('/')
def hello():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT id, name, url, source, facebook_id, logo FROM meetups")
    rows = cur.fetchall()
    data = []
    for meetup in rows:
        try:
            cur.execute("SELECT name, url, event_date FROM events WHERE events.meetup_id = %d ORDER BY event_date DESC LIMIT 1" % meetup['id'])
            next_event_db = cur.fetchall()
            next_event = {
                'event_name': next_event_db[0][0],
                'event_date': datetime.strftime(next_event_db[0][2], '%d.%m.%Y'),
                'event_url': next_event_db[0][1],
                'html': html(next_event_db[0])
            }
        except IndexError:
            next_event = None
        meetup_data = {'url': meetup['url'],
             'logo': meetup['logo'],
             'meetup_name': meetup['name'],
             'next_event': next_event
            }
        data.append(meetup_data)
    cur.execute("SELECT updated_at FROM updates ORDER BY updated_at DESC LIMIT 1")
    updated = datetime.strftime(cur.fetchall()[0][0], '%d.%m.%Y %H:%M:%S')
    meetups = sorted(data, key=lambda x: x['meetup_name'])
    return render_template('index.html', meetups=meetups, updated=updated)


def html(next_event):
    return '<i class="fa fa-calendar"></i> %s %s' % (datetime.strftime(next_event[2], '%d.%m.%Y'), next_event[0])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 37412))
    app.run(host='0.0.0.0', port=port)
