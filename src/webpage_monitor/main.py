from datetime import datetime, timedelta
from dateutil import parser
from os.path import join
from tenyks.client import Client, run_client
from tenyks.client.config import settings
import sqlite3, requests

class TenyksWebpageMonitor(Client):

    irc_message_filters = {
        'add_url': [r'add url (.*)'],
        'list_url': r'list url',
        'del_url': r'delete url (.*)',
    }
    direct_only = True
    recurring_delay = 30

    def __init__(self, *args, **kwargs):
        super(TenyksWebpageMonitor, self).__init__(*args, **kwargs)
        self.create_tables(self.fetch_cursor())

    def fetch_cursor(self):
        db_file = 'eccentric_garbanzo.db'
        print "DB in {}".format(join(settings.WORKING_DIR, db_file))
        conn = sqlite3.connect(join(settings.WORKING_DIR, db_file))
        return conn.cursor()

    def handle(self, I, Dont, Care):
        pass

    def recurring(self):
        self.logger.debug('Checking pages')
        cur = self.fetch_cursor()
        for channel in self.get_channels(cur):
            connection = self.get_connection(cur, channel)
            for url in self.urls_by_channel(cur, channel):
                self.url_handler(cur, url, channel, connection)

    def handle_list_url(self, data, match):
        self.logger.debug('list_urls')
        cur = self.fetch_cursor()
        connection = self.get_or_create_connection(
                cur, data['connection'])
        channel = self.get_or_create_channel(
                cur, connection, data['target'])
        url_sql = """
            SELECT * FROM url
            WHERE channel_id = ?"""
        result = cur.execute(url_sql, (channel[0],)).fetchone()
        if not result:
            self.send('No urls monitored.', data)
        else:
            self.send('URLs for this channel:', data)
            for i, feed in enumerate(cur.execute(url_sql, (channel[0],))):
                self.send('{i}. {url}'.format(i=i+1,
                    url=feed[1]), data)

    def url_handler(self, cur, url, channel, connection):
        self.logger.debug('Checking: {}'.format(url[1]))
        should_send_alert = False
        error = None
        r = None

        try:
            r = requests.get(url[1])
        except requests.ConnectionError:
            error = " is unreachable!"

        if r and r.status_code in [500, 404, 502, 503, 504, 401]:
            error = " is returning bad codes!"

        alert = self.get_most_recent_alert(cur, url[0])

        if alert:
            timestamp = parser.parse(alert[1])
            should_send_alert = datetime.utcnow() > timestamp + timedelta(minutes=10)

        if error is not None and should_send_alert:
            message = "\x034ALERT\x03: {url}{error} Code: {code}".format(
                url=url[1], error=error, code=getattr(r, "status_code", "N/A"))
            data = {
                'command': 'PRIVMSG',
                'client': self.name,
                'payload': message,
                'target': channel[1],
                'connection': connection[1],
            }
            if channel[1].startswith('#'):
                data['private_message'] = False
            else:
                data['private_message'] = True
                data['nick'] = channel[1]
            result = cur.execute("""
                INSERT INTO alert (url_id)
                VALUES (?)
            """, (url[0],))
            cur.connection.commit()
            self.send(message, data)

    def handle_add_url(self, data, match):
        if data['admin']:
            url = match.groups()[0]
            self.logger.debug('add_url: {}'.format(url))
            cur = self.fetch_cursor()
            connection = self.get_or_create_connection(cur,
                    data['connection'])
            if data['private_message']:
                target = data['nick']
            else:
                target = data['target']
            channel = self.get_or_create_channel(cur,
                    connection, target)
            url = self.get_or_create_url(cur, channel, url)
            self.send('{} is now monitored.'.format(url[1]), data)

    def handle_del_url(self, data, match):
        if data['admin']:
            url = match.groups()[0]
            self.logger.debug('del_url: {}'.format(url))
            cur = self.fetch_cursor()
            connection = self.get_or_create_connection(cur,
                data['connection'])
            channel = self.get_or_create_channel(cur,
                connection, data['target'])
            if self.url_exists(cur, url, channel):
                self.delete_url(cur, url, channel)
                self.send('{} is now deleted.'.format(url), data)
            else:
                self.send('{} did not exist.'.format(url), data)

    def url_exists(self, cur, url, channel):
        result = cur.execute("""
            SELECT * FROM url
            WHERE channel_id = ?
            AND url = ?
        """, (channel[0], url))
        return result.fetchone() is not None

    def delete_url(self, cur, url, channel):
        result = cur.execute("""
            DELETE FROM url
            WHERE channel_id = ?
            AND url = ?
        """, (channel[0], url))
        cur.connection.commit()

    def get_db(self):
        db_file = '{name}.db'.format(name=self.name)
        return sqlite3.connect(join(settings.WORKING_DIR, db_file))

    def get_most_recent_alert(self, cur, url):
        result = cur.execute("""
            SELECT * FROM alert WHERE url_id = ? ORDER BY created_at DESC;
        """, (url,))
        return result.fetchone()

    def get_channels(self, cur):
        result = cur.execute("""
            SELECT * FROM channel
        """)
        return result.fetchall()

    def get_connection(self, cur, channel):
        return cur.execute("""
            SELECT * FROM connection
            WHERE id = ?""", (channel[2],)).fetchone()

    def get_or_create_channel(self, cur, connection, channel_name):
        channel_sql = """
            SELECT * FROM channel
            WHERE channel = ?
            AND connection_id = ?"""
        result = cur.execute(channel_sql, (channel_name, connection[0]))
        channel = result.fetchone()
        if not channel:
            result = cur.execute("""
            INSERT INTO channel (channel, connection_id)
            VALUES (?, ?)""", (channel_name, connection[0]))
            result = cur.execute(channel_sql, (channel_name, connection[0]))
            cur.connection.commit()
            channel = result.fetchone()
        return channel

    def get_or_create_url(self, cur, channel, passed_url):
        url_sql = """
            SELECT * FROM url
            WHERE channel_id = ?
            AND url = ?
        """
        result = cur.execute(url_sql, (channel[0], passed_url))
        url = result.fetchone()
        if not url:
            result = cur.execute("""
            INSERT INTO url (channel_id, url)
            VALUES (?, ?)""", (channel[0], passed_url))
            cur.connection.commit()
            result = cur.execute(url_sql, (channel[0], passed_url))
            url = result.fetchone()
        return url

    def get_or_create_connection(self, cur, name):
        connection_sql = """
            SELECT *
            FROM connection
            WHERE connection_name = ?"""
        result = cur.execute(connection_sql, (name,))
        connection = result.fetchone()
        if not connection:
            result = cur.execute("""
                INSERT INTO connection (connection_name)
                VALUES (?)
            """, (name,))
            result = cur.execute(connection_sql, (name,))
            cur.connection.commit()
            connection = result.fetchone()
        return connection

    def urls_by_channel(self, cur, channel):
        result = cur.execute("""
            SELECT * FROM url
            WHERE channel_id = ?""", (channel[0],))
        return result.fetchall()

    def create_tables(self, db):
        table_sql = """
        CREATE TABLE IF NOT EXISTS alert (
            id INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            url_id INTEGER,
            FOREIGN KEY(url_id)
                REFERENCES url(id)
        );
        CREATE TABLE IF NOT EXISTS url (
            id INTEGER PRIMARY KEY,
            url TEXT,
            channel_id INTEGER,
            FOREIGN KEY(channel_id)
                REFERENCES channel(id)
        );
        CREATE TABLE IF NOT EXISTS connection (
            id INTEGER PRIMARY KEY,
            connection_name TEXT
        );
        CREATE TABLE IF NOT EXISTS channel (
            id INTEGER PRIMARY KEY,
            channel TEXT,
            connection_id INTEGER,
            FOREIGN KEY(connection_id)
                REFERENCES connection(id)
        );
        """
        db.executescript(table_sql)


def main():
    run_client(TenyksWebpageMonitor)

if __name__ == '__main__':
    main()
