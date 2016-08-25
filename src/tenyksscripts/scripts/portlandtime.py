from datetime import datetime
from dateutil.tz import tzlocal
import pytz
import random

def run(data, settings):
    if data['payload'] == 'portland time':
        if random.random() > 0.3:
            tz = pytz.timezone('America/Los_Angeles')
            now = datetime.now(tzlocal())
            now.replace(tzinfo=tz)
            return now.astimezone(tz).strftime('%X')
        else:
            return "Don't you know?"
