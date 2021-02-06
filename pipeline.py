import sqlite3

from items import Appearance, Disc

class Sqlite3Pipeline(object):
    result_conn = sqlite3.connect('data.sqlite')

    def __init__(self, *args, **kwargs):
        super(Sqlite3Pipeline, self).__init__(*args, **kwargs)
        self.result_conn.execute('DROP TABLE IF EXISTS appearance')
        self.result_conn.execute('DROP TABLE IF EXISTS disc')

        self.result_conn.execute('''
            CREATE TABLE appearance (
                id TEXT PRIMARY KEY,
                broadcast_time DATETIME NOT NULL,
                guest_name TEXT NOT NULL
            )
        ''')

        self.result_conn.execute('''
            CREATE TABLE disc (
                appearance_id TEXT,
                artist TEXT,
                title TEXT NOT NULL,
                position INTEGER NOT NULL,
                FOREIGN KEY(appearance_id) REFERENCES appearance(id)
            )
        ''')

        self.result_conn.commit()

    def process_item(self, item, spider):
        if type(item) == Appearance:
            self.result_conn.execute('''
                INSERT INTO appearance (id, broadcast_time, guest_name) VALUES (?, ?, ?)
            ''', (item['id'], item['broadcast_time'], item['guest_name']))

        if type(item) == Disc:
            self.result_conn.execute('''
                INSERT INTO disc (appearance_id, artist, title, position) VALUES (?, ?, ?, ?)
            ''', (item['appearance_id'], item['artist'], item['title'], item['position']))

        self.result_conn.commit()

        return item

