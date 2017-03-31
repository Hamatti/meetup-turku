from datetime import datetime


class Event(object):

    def __init__(self):
        self.meetup_name = ''
        self.meetup_url = ''
        self.event_name = ''
        self.event_date = ''
        self.event_url = ''

    def __str__(self):
        return '[{meetup}] {event_name} @ {event_date}'.format(
                meetup=self.meetup_name,
                event_name=self.event_name,
                event_date=self.date)

    def __repr__(self):
        return '[{meetup}] {event_name} @ {event_date}'.format(
                meetup=self.meetup_name,
                event_name=self.event_name,
                event_date=self.date)

    def html(self):
        template = '<i class="fa fa-calendar"></i> {event_date} {event_name}'
        return template.format(
                event_date=self.date,
                event_name=self.event_name)

    def to_json(self):
        return {
            'event_name': self.event_name,
            'event_url': self.event_url,
            'event_date': self.date,
            'html': self.html()
        }

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
        self.logo = meetup_data.get('logo')

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
