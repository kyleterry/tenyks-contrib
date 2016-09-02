import datetime
import requests
import time


def run(data, settings):
    if data["payload"] not in ["nextlaunch", "next launch", "smooth baby rocket", "WHOOOOOOOOOOOOOSH"]:
        return

    launches = requests.get("https://launchlibrary.net/1.2/launch", params={"next": 1, "mode": "verbose"}).json()
    if not launches["count"]:
        return "No launches scheduled"

    launch = launches["launches"][0]
    delta = datetime.timedelta(seconds=launch["netstamp"] - int(time.time()))

    return "Next launch: {name}. When: {time} (in {delta})".format(
        name=launch["name"],
        time=launch["net"],
        delta=delta
    )
