# Meetups in Turku web site application

*Flask application to fetch and show the upcoming tech meetups in Turku*

To use, you should have [a virtualenv](https://virtualenv.pypa.io/en/stable/).

```
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To run `get_events.py` you need API tokens for Facebook and Meetup.com as
enviromental variables.

```
$ export FBTOKEN='[yourtoken]'
$ export MEETUPTOKEN='[yourtoken]'
```

Then run the flask app

```
$ python app.py
```


