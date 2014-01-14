import requests


def run(data, settings):
    if 'user_stats ' in data['payload']:
        url = None
        requested_user = data['payload'].split("user_stats ")[1]
        if data['target'] == '#merveilles':
            url = 'http://merveill.es/data/{}'.format(requested_user)
        else:
            url = 'http://{chan}.shithouse.tv/data/{user}'.format(
                chan=data['target'].strip("#"), user=requested_user)

        response = requests.get(url).json()

        if data["total_posts"] == 0:
            return "No data on that user."
        return "Links: {} First Link: {} Most recent link: {} Average links per hour: {}".format(
            data["total_posts"], data["first_post_date"], data["most_recent_post"], data["average_posts_per_hour"])

