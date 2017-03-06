from datetime import datetime

class Event(object):

    def __init__(self):
        self.meetup_name = ''
        self.meetup_url = ''
        self.event_name = ''
        self.event_date = ''

    def __str__(self):
        return '[{meetup}] {event_name} @ {event_date}'.format(meetup=self.meetup_name,
                event_name=self.event_name, event_date=self.date)

    def __repr__(self):
        return '[{meetup}] {event_name} @ {event_date}'.format(meetup=self.meetup_name,
                event_name=self.event_name, event_date=self.date)

    @property
    def date(self):
        return datetime.strftime(self.event_date, '%d.%m.%Y')

class Meetup(object):

    def __init__(self, meetup_data):
        from parsers import FacebookParser, MeetabitParser, MeetupParser

        self.name = meetup_data.get('name')
        self.url = meetup_data.get('meetup_url')
        self.fb_id = meetup_data.get('facebook_id')
        self.source_type = meetup_data.get('url_source')

        if self.source_type == 'facebook':
            self.parser = FacebookParser(self)
        elif self.source_type == 'meetabit':
            self.parser = MeetabitParser(self)
        elif self.source_type == 'meetup':
            self.parser = MeetupParser(self)

        self.future_events = []

    def get_events(self):
        self.parser.parse()

    @property
    def next_event(self):
        return self.parser.next_event

    def __repr__(self):
        return '{name}'.format(name=self.name)


