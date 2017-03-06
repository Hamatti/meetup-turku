from parsers import FacebookParser, MeetabitParser, MeetupParser
import meetupdirectory
from models import Meetup

all_meetups = meetupdirectory.meetups

test_facebook = False
test_meetabit = False
test_meetup = True

if test_facebook:
    print 'Testing Facebook meetups'

    meetups = [Meetup(mt) for mt in all_meetups if mt['url_source'] == 'facebook']
    for meetup in meetups:
        meetup.get_events()
        print meetup
        print meetup.next_event

if test_meetabit:
    print 'Testing Meetabit meetups'
    meetups = [Meetup(mt) for mt in all_meetups if mt['url_source'] == 'meetabit']
    for meetup in meetups:
        meetup.get_events()
        print meetup
        print meetup.next_event


if test_meetup:
    print 'Testing Meetup.com meetups'
    meetups = [Meetup(mt) for mt in all_meetups if mt['url_source'] == 'meetup']
    for meetup in meetups:
        meetup.get_events()
        print meetup
        print meetup.next_event
