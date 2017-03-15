from facebook import GraphAPI
from datetime import datetime
import meetupdirectory
from urlparse import urlparse
from bs4 import BeautifulSoup
import json
from urllib2 import urlopen
import os
import meetup.api

from models import Event

class Parser(object):

    def __init__(self, url=None):
        self.url = url

    def parse(self):
        pass


class FacebookParser(Parser):

    def __init__(self, meetup):
        self.meetup = meetup
        self.accesstoken = os.getenv('FBTOKEN')
        self.url = meetup.url
        if meetup.fb_id:
            self.facebook_id = meetup.fb_id
        else:
            self.facebook_id = self.get_facebook_id()
        self.graph = GraphAPI(access_token=self.accesstoken,version='2.7')

    def parse(self):
        self.fb_api()

    def get_facebook_id(self):
        fb_id = self.url.split('/')[4]
        try:
            fb_id = int(fb_id)
        except ValueError:
            print 'Only works with numeric ids currently'
            return None

        return fb_id

    def fb_api(self):
        if not self.facebook_id:
            self.future_events = []
            return
        events = self.graph.get_connections(self.facebook_id, connection_name='events')['data']

        time_now = datetime.now()
        if not events:
            self.next_event = None
        else:
            next_event_data = events[0]
            date = datetime.strptime(next_event_data['start_time'][:-5], '%Y-%m-%dT%H:%M:%S')
            if date < time_now:
                self.next_event = None
                return
            self.next_event = Event()
            self.next_event.meetup_name = self.meetup.name
            self.next_event.meetup_url = self.meetup.url
            self.next_event.event_name = next_event_data['name']
            self.next_event.event_date = date
            self.next_event.event_url = 'https://facebook.com/events/%s' % next_event_data['id']

    def parse_time(self, timestamp):
        return datetime.strptime(timestamp[:-5], '%Y-%m-%dT%H:%M:%S')


class MeetabitParser(Parser):
    api_url = 'https://meetabit.unit.run/events?{id}'

    def __init__(self, meetup):
        self.meetup = meetup
        self.url = meetup.url
        self.meetabit_id = urlparse(self.url).path.split('/')[-1]

    def parse(self):
        soup = BeautifulSoup(urlopen(MeetabitParser.api_url.format(id=self.meetabit_id)))
        events = json.loads(soup.string)
        self.future_events = [ev for ev in events['results'] if ev['past'] == False]
        if self.future_events:
            next_event = self.future_events[0]
            current_year = datetime.now().year
            self.next_event = Event()
            self.next_event.event_date = datetime.strptime('%s/%s' % (next_event['date'], current_year), '%d/%m/%Y')
            self.next_event.event_name = next_event['name']
            self.next_event.meetup_name = self.meetup.name
            self.next_event.meetup_url = self.meetup.url
            self.next_event.event_url = next_event['url']
        else:
            self.next_event = None


class MeetupParser(Parser):

    def __init__(self, _meetup):
        self.meetup = _meetup
        self.url = _meetup.url
        self.accesstoken = os.getenv('MEETUPTOKEN')
        self.urlname = urlparse(self.url).path.strip('/')
        self.client = meetup.api.Client(self.accesstoken)
        self.future_events = []

    def parse(self):
        next_event = self.client.GetGroup({'urlname': self.urlname}).next_event
        event = Event()
        event.event_name = next_event['name']
        event.event_date = datetime.fromtimestamp(next_event['time']/1000)
        event.meetup_name = self.meetup.name
        event.meetup_url = self.meetup.url

        event_id = next_event['id']
        event.event_url = 'https://www.meetup.com/%s/events/%s/' % (self.urlname, event_id)
        self.next_event = event
