from datetime import datetime
from dateutil.tz import tzlocal
import pytz


def run(data, settings):
    if data['payload'] == 'jnerula time':
        pdx = ''.join(map(chr, filter(None, [65,109,101,114,105,99,97,47,76,111,115,95,65,110,103,101,108,101,115])))
        tz = pytz.timezone(pdx)
        now = datetime.now(tzlocal())
        now.replace(tzinfo=tz)
        return now.astimezone(tz).strftime('%a %b %d %X %z')
