import requests
import json
from datetime import datetime, timedelta
from random import randint
import pytz

from interval import setInterval
from client import Client

client = Client.instance()

local = pytz.timezone ("Asia/Seoul")

def fetch_push(URL, parsed_func, interval, **kargs):
    def func():
        try:
            res = requests.get(URL)
        except requests.exceptions.ConnectionError:
            return

        body = json.loads(res.text)
        
        data = parsed_func(body, **kargs)

        try: 
            client.write_points(data)
        except requests.exceptions.ConnectionError:
            return

    setInterval(func, interval)

def convert_to_utc(timestamp, format):
    naive = datetime.strptime(timestamp, format)
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    return utc_dt # utc_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def add_random_time(timestamp):
    return timestamp + timedelta(microseconds=(randint(1, 1000)))