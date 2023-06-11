from functools import partial
from geopy.geocoders import Nominatim

import datetime
import dateparser

import requests

def get_coord(city):
    geolocator = Nominatim(user_agent="rzd")
    geocode = partial(geolocator.geocode, language="ru")
    res = geocode(city)
    if not res:
        return (0, 0)

    return ((res.latitude, res.longitude))

def get_next_days(today, count_days):
    date_obj = dateparser.parse(today, date_formats=['%d.%m.%Y'])
    date_obj += datetime.timedelta(days=count_days)
    date_string = date_obj.strftime('%d.%m.%Y')
    return date_string

def convert_date(today):
    date_obj = dateparser.parse(today, date_formats=['%d.%m.%Y'])
    return date_obj.strftime('%Y-%m-%d')

def get_random_date(today):
    deadline_date = get_next_days(today, 45)
    data = {
        'start' : convert_date(today),
        'end' : convert_date(deadline_date)
    }
    r = requests.post('https://randomall.ru/api/general/date', json=data)
    return r.text[1:-1]

def get_today():
    return datetime.datetime.now().strftime("%d.%m.%Y")