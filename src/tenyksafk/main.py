import sqlite3
from os.path import join
from tenyksservice import TenyksService, run_service
from tenyksservice.config import settings

class AFK(TenyksService):
    direct_only = False
    irc_message_filters = {
        'depart': [r'^(?i)(xopa|away|afk|brb)'],
        'return': [r'^(?i)(xoka|back)'],
        'query': [r'(?P<nick>(.*))\?$'],
        'list': [r'list']
    }

    def __init__(self, *args, **kwargs):
        super(AFK, self).__init__(*args, **kwargs)
        self.create_tables(self.fetch_cursor())

    def handle_depart(self, data, match):
        nick = data['nick']

        if not self.user_exists(self.fetch_cursor(), nick):
            self.create_user(self.fetch_cursor(), nick, True)

        if not self.user_away(self.fetch_cursor(), nick):
            self.send('{nick} is now AFK.'.format(nick=nick), data) 

        self.user_depart(self.fetch_cursor(), nick)

    def handle_return(self, data, match):
        nick = data['nick']

        if not self.user_exists(self.fetch_cursor(), nick):
            self.create_user(self.fetch_cursor(), nick, False)

        if self.user_away(self.fetch_cursor(), nick):
            self.send('{nick} is no longer AFK.'.format(nick=nick), data)

        self.user_return(self.fetch_cursor(), nick)

    def handle_query(self, data, match):
        nick = match.groupdict()['nick']

        if self.user_exists(self.fetch_cursor(), nick):
            status = 'AFK' if self.user_away(self.fetch_cursor(), nick) else 'present'
            self.send('{nick} is currently {status}.'.format(nick=nick, status=status), data)
        else:
            self.send('{nick}\'s status is unknown.'.format(nick=nick), data)

    def handle_list(self, data, match):
        afkers = self.fetch_afk(self.fetch_cursor())

        if len(afkers) == 0:
            self.send('There are currently no AFKers.', data)
        else:
            self.send('AFKers: {afk}'.format(afk=', '.join('%s' % nick for nick in afkers)), data)

    def create_tables(self, cur):
        table_sql = '''
        CREATE TABLE IF NOT EXISTS afkers (
            id INTEGER PRIMARY KEY,
            nick TEXT,
            away BOOLEAN
        );
        '''
        cur.executescript(table_sql)

    def fetch_cursor(self):
        db_file = '{name}.db'.format(name=self.name)
        conn = sqlite3.connect(join(settings.WORKING_DIR, db_file))
        return conn.cursor()

    def create_user(self, cur, nick, away=False):
        result = cur.execute('''
            INSERT INTO afkers (nick, away)
            VALUES (?, ?)
        ''', (nick, away))
        result.connection.commit()

    def user_exists(self, cur, nick):
        result = cur.execute('''
            SELECT * FROM afkers
            WHERE nick = ?
        ''', (nick,))
        return result.fetchone() is not None

    def user_depart(self, cur, nick):
        result = cur.execute('''
            UPDATE afkers SET away = ?
            WHERE nick = ?
        ''', (True, nick))
        result.connection.commit()

    def user_return(self, cur, nick):
        result = cur.execute('''
            UPDATE afkers SET away = ?
            WHERE nick = ?
        ''', (False, nick))
        result.connection.commit()

    def user_away(self, cur, nick):
        result = cur.execute('''
            SELECT away from afkers
            WHERE nick = ?
        ''', (nick,))
        return result.fetchone()[0]

    def fetch_afk(self, cur):
        result = cur.execute('''
            SELECT nick FROM afkers
            WHERE away = 1
            ORDER BY nick ASC
        ''')
        return result.fetchall();


def main():
    run_service(AFK)


if __name__ == '__main__':
    main()
