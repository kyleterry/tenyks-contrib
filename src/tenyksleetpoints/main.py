import sqlite3
from os.path import join

from tenyksclient.client import Client, run_client
from tenyksclient.config import settings


class TenyksLeetPoints(Client):
    irc_message_filters = {
        'add_points': [r'add points (?P<user>.*) (?P<points>[0-9]*)', r'(?P<user>.*) \+(?P<points>[0-9]*) (.*)'],
        'remove_points': [r'remove points (.*) (.*)',r'\+([0-9]*) (.*)'],
        'highscore': [r'highscore', r'scores', r'highscores'],
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
        if self.conspirator_exists(self.fetch_cursor()):
            if data['nick'] != match.groups():
                self.increment_points(self.fetch_cursor(), int(match.groups)
            else:
                self.send("Cannot add points to yourself.", data)
        else:
            self.create_conspirator(self.fetch_cursor(), 

        self.send("test", data)

    def handle_remove_points(self, data, match):
        self.send("test", data)

    def handle_highscore(self, data, match):
        self.send("Highscores: ", data)
        for person in self.fetch_conspirators(self.fetch_cursor()):
            self.send("{0}: {1}".fornmat(person[0], person[1]), data)

    def fetch_conspirators(self, cur):
        result = cur.execute("""
            SELECT * FROM points
            ORDER BY points,person DESC;
        """)
        return result.fetchall()

    def conspirator_exists(self, cur, person_name):
        result = cur.execute("""
            SELECT * FROM points
            WHERE person = ?
        """, (person_name))
        return result.fetchone() is not None

    def create_conspirator(self, cur, name):
        result = cur.execute("""
            INSERT INTO points (person, points)
            VALUES (?, ?)
        """, (name, 0))
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
