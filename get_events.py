import json, os
import meetupdirectory
from models import Meetup
from datetime import datetime

def get_events():
    meetups = []
    for meetup in meetupdirectory.meetups:
        mt = Meetup(meetup)
        mt.get_events()
        meetups.append(mt)
    return meetups

def write_events(meetups):
    data = {}
    data['updated'] = datetime.strftime(datetime.now(), '%d.%m.%Y %H:%M')
    next_events = []
    for meetup in meetups:
        event = {
            'meetup_name': meetup.name,
            'logo': meetup.logo,
            'url': meetup.url,
            'next_event': None
        }
        if meetup.next_event:
            event['next_event'] = meetup.next_event.to_json()
        next_events.append(event)

    data['data'] = next_events
    cur_path = os.path.dirname(os.path.realpath(__file__))
    outfile = os.path.join(cur_path, 'next_events.json')
    print outfile
    json.dump(data, open(outfile, 'w'))

if __name__ == '__main__':
    meetups = get_events()
    write_events(meetups)
