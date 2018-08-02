import os
import psycopg2
import jwt
import pprint as p
from psycopg2 import connect
from flask import current_app
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

from .createdb import connect_to_db

conn = connect_to_db(current_app.config.get('APP_SETTINGS'))
conn.set_session(autocommit=True)
cur = conn.cursor()


class Base():
    '''Base class to set up database'''

    def save(self):
        conn.commit()

    @staticmethod
    def get(table_name, **kwargs):
        for key, val in kwargs.items():
            sql = "SELECT * FROM {} WHERE {}='{}'".format(table_name, key, val)
            cur.execute(sql)
            item = cur.fetchone()
            return item

    @staticmethod
    def get_all(table_name):
        sql = 'SELECT * FROM {}'.format(table_name)
        cur.execute(sql)
        data = cur.fetchall()
        return data

    @staticmethod
    def update(table, id, data):
        for key, val in data.items():
            string = "{}='{}'".format(key, val)
            sql = 'UPDATE {} SET {} WHERE id={}'.format(table, string, id)
            cur.execute(sql)
            conn.commit()

    @staticmethod
    def delete(table, id):
        sql = 'DELETE FROM {} WHERE id={}'.format(table, id)
        cur.execute(sql)
        conn.commit()


class User(Base):
    '''Class to model the user'''

    def __init__(self, username, email, password):
        '''Initialize user variables'''
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def add(self):
        '''Method for adding input into users table'''
        cur.execute(
            """
            INSERT INTO users(username, email, password)
            VALUES(%s,%s,%s)""",
            (self.username, self.email, self.password))
        self.save()

    @staticmethod
    def user_dict(user):
        '''Method for returning user details'''
        return dict(
            id=user[0],
            username=user[1],
            email=user[2]
        )

    @staticmethod
    def validate_password(password, username):
        '''Method for validating password input'''
        user = User.get('users', username=username)
        if check_password_hash(user[3], password):
            return True
        return False

    @staticmethod
    def generate_token(user):
        '''Method for generating a token upon login'''
        user_id, username = user[0], user[1]
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow()+timedelta(minutes=6000),
            'iat': datetime.utcnow()}
        token = jwt.encode(payload, str(
            current_app.config.get('SECRET')), algorithm='HS256')
        return token.decode()

    @staticmethod
    def decode_token(token):
        '''Method for decoding generated token'''
        payload = jwt.decode(token, str(
            current_app.config.get('SECRET')), algorithms=['HS256'])
        return payload


class Entry(Base):
    '''Class to model the entry'''

    def __init__(self, title, description, user_id):
        '''Initialize entry variables'''
        self.title = title
        self.description = description
        self.user_id = user_id
        self.created_at = datetime.utcnow().isoformat()
        self.last_modified = datetime.utcnow().isoformat()

    def add(self):
        '''Method for adding input into entries table'''
        cur.execute(
            """
            INSERT INTO entries (user_id, title, description, created_at, last_modified)
            VALUES (%s , %s, %s, %s, %s)
            """,
            (self.user_id, self.title, self.description, self.created_at, self.last_modified))
        self.save()

    @staticmethod
    def get(user_id, entry_id=None):
        '''Method for fetching both single and all entries'''
        if entry_id:
            cur.execute(
                """SELECT * FROM entries WHERE user_id={} AND id={}""".format(user_id, entry_id))
            return cur.fetchone()

        cur.execute(
            """SELECT
                entries.id,
                users.id,
                title,
                description,
                created_at,
                last_modified
            FROM users INNER JOIN entries ON entries.user_id=users.id WHERE users.id={}""".format(user_id))
        user_entries = cur.fetchall()
        return user_entries

    @staticmethod
    def verify_entries(title, description, user_id):
        """Checks for duplication of an entry"""
        sql = """SELECT entries.title, entries.description FROM entries
                  WHERE user_id = {} and title = '{}' and description = '{}'
               """.format(user_id, title, description)
        try:
            cur.execute(sql)
            data = cur.fetchone()
            if data:
                return data
            return "success"
        except:
            conn.rollback()

    @staticmethod
    def entry_dict(entry):
        '''Method for returning entry details'''
        return dict(
            id=entry[0],
            user_id=entry[1],
            title=entry[2],
            description=entry[3],
            created_at=entry[4].isoformat(),
            last_modified=entry[5].isoformat()
        )
