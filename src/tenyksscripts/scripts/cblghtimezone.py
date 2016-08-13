from datetime import datetime
from dateutil.tz import tzlocal
import pytz


def run(data, settings):
    if data['payload'] == 'cblgh time':
        tz = pytz.timezone('Europe/Stockholm')
        now = datetime.now(tzlocal())
        now.replace(tzinfo=tz)
        return now.astimezone(tz).strftime('%X')
