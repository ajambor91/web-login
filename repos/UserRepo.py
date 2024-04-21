from entities.User import User
import sqlite3
from db.DataBase import DataBase
from functions.db import entity
class UserRepo:

    def __init__(self):
        self.conn = DataBase()

    @entity
    def insert_user(self, user: User):
        cursor = self.conn.db_connect()
        cursor.execute('''INSERT INTO user (login, password)
                          VALUES (?, ?)''', (user.login, user.password))

    @entity
    def get_user(self, user: User):
        print('OPOPOPOPOPOPOP')
        cursor = self.conn.db_connect()
        cursor.execute('''SELECT login, password FROM user WHERE login = ? AND password = ? ''', (user.login, user.password))
        result = cursor.fetchone()
        print(result)
        print('oooooo')
        return result
