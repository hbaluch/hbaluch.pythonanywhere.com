import sqlite3
from sqlite3 import OperationalError

class UrlStorageUtility:

    def __init__(self, path = 'urls.db'):
        self.db_path = path
        self.__create_table()

    def __create_table(self):
        create_query = ''' CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY     AUTOINCREMENT, url TEXT NOT NULL)'''
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(create_query)
            except OperationalError:
                raise


    def insert_url_and_get_id(self, fullUrl):
        insert_query    = '''INSERT INTO urls (url) VALUES ('%s')''' % fullUrl

        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            try:
                resultant = cursor.execute(insert_query)
            except OperationalError:
                return 0
        return resultant.lastrowid

    def fetch_original_url(self, row_id):
        select_query = '''SELECT url FROM urls WHERE ID = %s'''%row_id
        original_url = 'INVALID'
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            try:
                resultant = cursor.execute(select_query)
            except OperationalError:
                raise
        try:
            original_url = resultant.fetchone()[0]
        except Exception as e:
            return 'INVALID'
        return original_url