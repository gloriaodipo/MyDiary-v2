# MyDiary-v2
MyDiary is an online journal where users can pen down their thoughts and feelings.

### Prerequisites

- [Python 3.6](https://www.python.org/downloads/release/python-360/)
- [Virtual Environment](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)
- [Flask](http://flask.pocoo.org/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)

### Endpoints

| METHOD | ENDPOINT                                      | DESCRIPTION                      |
| ------ | --------------------------------------------- | -------------------------------- |
| POST   | /api/v1/user/signup/                          | User registration                |
| POST   | /api/v1/user/login/                           | Login signed up user             |
| POST   | /api/v1/user/entries/                         | Create a new entry               |
| GET    | /api/v1/user/entries/<int:entry_id>/          | Fetch a single entry             |
| GET    | /api/v1/user/entries/                         | Fetch all entries                |
| PUT    | /api/v1/user/entries/<int:entry_id>/          | Modify an entry                  |
| DELETE | /api/v1/user/entries/<int:entry_id>/          | Delete an entry                  |

## Prerequisites

## Prerequisites
- [Python3](https://www.python.org/) (A programming language)
- [Flask](http://flask.pocoo.org/) (A Python microframework)
- [PostgreSQL](https://www.postgresql.org/docs/10/static/intro-whatis.html) (Database)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/) (Stores all dependencies used in the project)
- [Pivotal Tracker](www.pivotaltracker.com) (A project management tool)
- [Pytest](https://docs.pytest.org/en/latest/) (Framework for testing)


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
