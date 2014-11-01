import sqlite3
from os.path import join

from tenyksservice import TenyksService, run_service
from tenyksservice.config import settings


class TenyksLogger(TenyksService):
    def __init__(self, *args, **kwargs):
        super(TenyksLogger, self).__init__(*args, **kwargs)

        with self.get_db() as db:
            self.create_tables(db)

    def handle(self, data, match, command):
        with self.get_db() as db:
            connection = self.get_or_create_connection(db, data['connection'])
            channel_id = self.get_or_create_channel(db, connection, data['target'])

            host_id = self.get_or_create_by_name(db, 'host', data['host'])
            user_id = self.get_or_create_by_name(db, 'user', data['user'])
            nick_id = self.get_or_create_by_name(db, 'nick', data['nick'])

            self.create_message(db, channel_id, host_id, user_id, nick_id, data['command'], data['full_message'])

    def get_db(self):
        db_file = '{name}.db'.format(name=self.name)
        return sqlite3.connect(join(settings.WORKING_DIR, db_file))

    def get_or_create_connection(self, db, name):
        connection_sql = """
            SELECT *
            FROM connection
            WHERE connection_name = ?"""
        result = db.execute(connection_sql, (name,))
        connection = result.fetchone()
        if not connection:
            result = db.execute("""
                INSERT INTO connection (connection_name)
                VALUES (?)
            """, (name,))
            result = db.execute(connection_sql, (name,))
            connection = result.fetchone()
        return connection

    def get_or_create_channel(self, db, connection, channel_name):
        channel_sql = """
            SELECT id FROM channel
            WHERE channel = ?
            AND connection_id = ?"""
        result = db.execute(channel_sql, (channel_name, connection[0]))
        channel = result.fetchone()
        if not channel:
            result = db.execute("""
            INSERT INTO channel (channel, connection_id)
            VALUES (?, ?)""", (channel_name, connection[0]))
            result = db.execute(channel_sql, (channel_name, connection[0]))
            channel = result.fetchone()
        return channel[0]

    # NOTE: don't ever take `table` from user input
    def get_or_create_by_name(self, db, table, name):
        curs = db.cursor()

        sql = """
            SELECT id FROM %s
            WHERE name = ?""" % table
        result = curs.execute(sql, (name,))
        row = result.fetchone()

        if row:
            pk = row[0]
        else:
            result = curs.execute("""
            INSERT INTO %s (name)
            VALUES (?)""" % table, (name,))

            pk = curs.lastrowid

        return pk

    def create_message(self, db, channel_id, host_id, user_id, nick_id, command, message):
        result = db.execute("""
            INSERT INTO message (channel_id, host_id, user_id, nick_id, command, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (channel_id, host_id, user_id, nick_id, command, message))

    def create_tables(self, db):
        table_sql = """
        CREATE TABLE IF NOT EXISTS connection (
            id INTEGER PRIMARY KEY,
            connection_name TEXT
        );
        CREATE TABLE IF NOT EXISTS channel (
            id INTEGER PRIMARY KEY,
            channel TEXT,
            connection_id INTEGER,
            FOREIGN KEY(connection_id) REFERENCES connection(id)
        );
        CREATE TABLE IF NOT EXISTS host (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL
        );
        CREATE TABLE IF NOT EXISTS nick (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL
        );
        CREATE TABLE IF NOT EXISTS message (
            id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            host_id INTEGER,
            user_id INTEGER,
            nick_id INTEGER,
            command VARCHAR,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(channel_id) REFERENCES connection(id)
            FOREIGN KEY(host_id) REFERENCES host(id)
            FOREIGN KEY(user_id) REFERENCES user(id)
            FOREIGN KEY(nick_id) REFERENCES nick(id)
        );
        """
        db.executescript(table_sql)


def main():
    run_service(TenyksLogger)


if __name__ == '__main__':
    main()
