from entities.Page import Page
import sqlite3
from db.DataBase import DataBase
from functions.db import entity
class PageRepo:

    def __init__(self):
        self.conn = DataBase()

    @entity
    def insert_page(self, page: Page):
        cursor = self.conn.db_connect()
        cursor.execute('''INSERT INTO pages (link, data)
                          VALUES (?, ?)''', (page.link, page.data))

    @entity
    def get_pages(self):
        print('OPOPOPOPOPOPOP')
        cursor = self.conn.db_connect()
        cursor.execute('''SELECT link, data FROM pages''')
        result = cursor.fetchall()
        print(result)
        print('oooooo')
        return result
