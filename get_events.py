import json
import os
from datetime import datetime

import meetupdirectory
from models import Meetup

import psycopg2
import urlparse

urlparse.uses_netloc.append('postgres')
db_url = urlparse.urlparse(os.environ.get('DATABASE_URL'))

conn = psycopg2.connect(
    database=db_url.path[1:],
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname,
    port=db_url.port
)

conn.autocommit = True



def get_events():
    meetups = []
    cur = conn.cursor()
    cur.execute("SELECT name, url, source, facebook_id, logo, id FROM meetups")
    for _meetup in cur.fetchall():
        if _meetup[2] == 'facebook':
            pass
        meetup = {
            'name': _meetup[0],
            'meetup_url': _meetup[1],
            'url_source': _meetup[2],
            'logo': _meetup[4],
            'id': _meetup[5]
        }
        if _meetup[3]:
            meetup['facebook_id'] = _meetup[3]
        mt = Meetup(meetup)
        mt.get_events()
        meetups.append(mt)
    return meetups


def write_events(meetups):
    cur = conn.cursor()
    data = {}
    updated = datetime.strftime(datetime.now(), '%Y-%m-%d')
    for meetup in meetups:
        if meetup.next_event:
            ev = meetup.next_event
            name = ev.event_name
            url = ev.event_url
            date = datetime.strptime(ev.date, '%d.%m.%Y')
            meetup_id = meetup.id
            cur.execute('INSERT INTO events (meetup_id, name, url, event_date) VALUES (%d, \'%s\', \'%s\', \'%s\')' % (meetup_id, name, url, date))
        else:
            continue

    cur.execute('INSERT INTO updates (updated_at) VALUES (\'%s\')' % updated)
    cur.close()

if __name__ == '__main__':
    meetups = get_events()
    write_events(meetups)
    conn.close()
