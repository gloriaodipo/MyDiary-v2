# MyDiary-v2
MyDiary is an online journal where users can pen down their thoughts and feelings.

[![Build Status](https://travis-ci.org/gloriaodipo/MyDiary-v2.svg?branch=develop)](https://travis-ci.org/gloriaodipo/MyDiary-v2) [![Coverage Status](https://coveralls.io/repos/github/gloriaodipo/MyDiary-v2/badge.svg?branch=develop)](https://coveralls.io/github/gloriaodipo/MyDiary-v2?branch=develop)

## Prerequisites
- [Python3](https://www.python.org/) (A programming language)
- [Flask](http://flask.pocoo.org/) (A Python microframework)
- [PostgreSQL](https://www.postgresql.org/docs/10/static/intro-whatis.html) (Database)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/) (Stores all dependencies used in the project)
- [Pivotal Tracker](www.pivotaltracker.com) (A project management tool)
- [Pytest](https://docs.pytest.org/en/latest/) (Framework for testing)

### Other technologies used:
- Flask_restful
- Postman
- Psycopg2

### Endpoints

| METHOD | ENDPOINT                                        | DESCRIPTION                      |
| ------ | ---------------------------------------------   | -------------------------------- |
| POST   | '/api/v1/user/signup'                           | User registration                |
| POST   | '/api/v1/user/login '                           | Login signed up user             |
| POST   | '/api/v1/user/entries '                         | Create a new entry               |
| GET    | '/api/v1/user/entries/<int:entry_id>'           | Fetch a single entry             |
| GET    | '/api/v1/user/entries'                          | Fetch all entries                |
| PUT    | '/api/v1/user/entries/<int:entry_id>'           | Modify an entry                  |
| DELETE | '/api/v1/user/entries/<int:entry_id>'           | Delete an entry                  |


## Getting Started:

**To start this app, please follow the instructions below:**

**On your terminal:**

Install pip:

 $ sudo apt-get install python-pip

Clone this repository:

 $ git clone https://github.com/gloriaodipo/MyDiary-v2.git

Get into the root directory:

 $ cd MyDiary-v2/

Install virtualenv:

 $ pip install virtualenv

Create a virtual environment in the root directory:

 $ virtualenv -name of virtualenv-
  
 Note: If you do not have python3 installed globally, please run this command when creating a virtual environment:
 
 $ virtualenv -p python3 -name of virtualenv-

Activate the virtualenv:

 $ source name of virtualenv/bin/activate

Install the requirements of the project:

 $ pip install -r requirements.txt

Create two databases, one for testing environment and one for development envronnment,as follows:

  $ createdb diary
  
  $ createdb testdb

To run tests:

 $ pytest
 
To run the app:

 $ Python run.py
