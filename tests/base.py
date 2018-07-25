import json
from unittest import TestCase
from app.createdb import connect_to_db
from app import create_app

SIGNUP_URL = '/api/v1/user/signup'
LOGIN_URL = '/api/v1/user/login'

class BaseTestClass(TestCase):
    '''Base class with setup for tests'''
    
    def setUp(self):
        conn = connect_to_db('testing')
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        cur.execute("""DROP TABLE IF EXISTS users CASCADE""" )
        cur.execute("""DROP TABLE IF EXISTS entries CASCADE""" )

        self.create_users_table(cur)
        self.create_entries_table(cur)
        
        self.app = create_app('testing')
        with self.app.app_context():
            from app.models import User, Entry
        self.client = self.app.test_client()

        self.entry_model = Entry
        self.user_model = User
       
        self.user_data = {
                    "username":"gloria", 
                    "email":"gloria@gmail.com",
                    "password":"password"
                    }
        self.entry_data = {
                    "title": "Freaky friday",
                    "description": "Fun fun fun fun fun fun"
                    }

        self.user1 = User(
            username='testuser',
            email='testuser@email.com',
            password='password')

        self.entry1 = Entry(
            title='I saved a dog',
            description='The dog was cute',
            user_id=1)

        self.test_user = User(
            username='gloria',
            email='glo@mail.com',
            password='password')

    def logged_in_user(self):
        # first create user
        self.client.post(SIGNUP_URL,
        data = json.dumps(self.user_data), content_type = 'application/json')

        # then log in user
        res = self.client.post(LOGIN_URL,
        data=json.dumps({'username': 'gloria', 'password': 'password'}),
        content_type='application/json')
        
        return res
    
    def create_users_table(self, cur):
        cur.execute(
            """CREATE TABLE users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL);""")
    
    def create_entries_table(self, cur):
        cur.execute(
            """CREATE TABLE entries(
                id serial,
                user_id INTEGER NOT NULL,
                title VARCHAR NOT NULL,
                description VARCHAR NOT NULL,
                created_at timestamp NOT NULL,
                last_modified timestamp NOT NULL,
                PRIMARY KEY (user_id , id),
                FOREIGN KEY (user_id) REFERENCES users (id));""")

    def tearDown(self):
        conn = connect_to_db('testing')
        cur = conn.cursor()
        cur.close()
        conn.commit()
        conn.close()
        