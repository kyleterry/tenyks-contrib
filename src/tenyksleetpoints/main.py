import sqlite3
from os.path import join
import requests

from tenyksservice import TenyksService, run_service, FilterChain
from tenyksservice.config import settings


class TenyksLeetPoints(TenyksService):
    irc_message_filters = {
        'add_points': FilterChain(
            [r'^(give|\+)\s*(?P<points>[0-9]*)\s*(point[s]*)* to (?P<nick>[a-zA-Z0-9-_`]*)\s*$'],
            direct_only=True),
        'remove_points': FilterChain(
            [r'^(take|\-)\s*(?P<points>[0-9]*)\s*(point[s]*)* from (?P<nick>[a-zA-Z0-9-_`]*)\s*$'],
            direct_only=True),
        'highscore': FilterChain(
            [r'high scores', r'highscore', r'scores', r'highscores',
             'what are everyone\'s points?'], direct_only=True)
    }

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
        resp = requests.post('http://ix.io?f:0={}'.format(
            ''.join(['{} {}\n'.format(i[1], i[2])
                  for i in self.fetch_conspirators(self.fetch_cursor())])))
        self.send('Highscores: {}'.format(resp.content), data)

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
    run_service(TenyksLeetPoints)

if __name__ == '__main__':
    main()
