import sqlite3
from os.path import join

from tenyks.client import Client, run_client
from tenyks.client.config import settings


class TenyksLeetPoints(Client):
    irc_message_filters = {
        'add_points': [r'^give (?P<points>[0-9]*) points to (?P<nick>[a-zA-Z0-9-_`]*)$',
                       r'^\+(?P<points>[0-9]*) to (?P<nick>[a-zA-Z0-9-_`]*)$'],
        'remove_points': [r'^remove (?P<points>[0-9]*) points from (?P<nick>[a-zA-Z0-9-_`]*)$',
                          r'^\-(?P<points>[0-9]*) to (?P<nick>[a-zA-Z0-9-_`]*)$'],
        'highscore': [r'highscore', r'scores', r'highscores', 'what are everyone\'s points?'],
    }
    direct_only = True

    def __init__(self, *args, **kwargs):
        super(TenyksLeetPoints, self).__init__(*args, **kwargs)
        self.create_tables(self.fetch_cursor())

    def fetch_cursor(self):
        db_file = '{name}.db'.format(name=self.name)
        conn = sqlite3.connect(join(settings.WORKING_DIR, db_file))
        return conn.cursor()

    def handle_add_points(self, data, match):
        match_dict = match.groupdict()

        if data['nick'] == match_dict['nick']:
            self.send('{nick}: You cannot give points to yourself.'.format(
                nick=data['nick']), data)
            return

        if not self.conspirator_exists(self.fetch_cursor(), match_dict['nick']):
            self.create_conspirator(self.fetch_cursor(), match_dict['nick'])

        self.increment_points(self.fetch_cursor(), match_dict['nick'],
            int(match_dict['points']))

        self.send('{nick}: Done.'.format(nick=data['nick']), data)

    def handle_remove_points(self, data, match):
        match_dict = match.groupdict()

        if data['nick'] == match_dict['nick']:
            self.send('{nick}: You cannot remove points from yourself.'.format(
                nick=data['nick']), data)
            return

        if not self.conspirator_exists(self.fetch_cursor(), match_dict['nick']):
            self.create_conspirator(self.fetch_cursor(), match_dict['nick'])

        self.decrement_points(self.fetch_cursor(), match_dict['nick'],
            int(match_dict['points']))

        self.send('{nick}: Done.'.format(nick=data['nick']), data)

    def handle_highscore(self, data, match):
        self.send("Highscores: ", data)
        for person in self.fetch_conspirators(self.fetch_cursor()):
            self.send("{0}: {1}".format(person[1], person[2]), data)

    def increment_points(self, cur, nick, points):
        result = cur.execute("""
            UPDATE points SET points = points.points + ?
            WHERE person = ?
        """, (points, nick))
        result.connection.commit()

    def decrement_points(self, cur, nick, points):
        result = cur.execute("""
            UPDATE points SET points = points.points - ?
            WHERE person = ?
        """, (points, nick))
        result.connection.commit()

    def fetch_conspirators(self, cur):
        result = cur.execute("""
            SELECT * FROM points
            ORDER BY points DESC;
        """)
        return result.fetchall()

    def conspirator_exists(self, cur, person_name):
        result = cur.execute("""
            SELECT * FROM points
            WHERE person = ?
        """, (person_name,))
        return result.fetchone() is not None

    def create_conspirator(self, cur, name, points=None):
        result = cur.execute("""
            INSERT INTO points (person, points)
            VALUES (?, ?)
        """, (name, points or 0))
        result.connection.commit()

    def create_tables(self, cur):
        table_sql = """
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY,
            person TEXT,
            points INTEGER
        );
        """
        cur.executescript(table_sql)

def main():
    run_client(TenyksLeetPoints)

if __name__ == '__main__':
    main()
