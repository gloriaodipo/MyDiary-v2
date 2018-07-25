from functools import wraps
from flask import request
from .models import User

def token_required(func):
    '''checks validity of tokens'''
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token = None
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                access_token = authorization_header.split(' ')[1]
            if access_token:
                user_id = User.decode_token(access_token)['user_id']
                return func(user_id=user_id, *args, **kwargs)
            return {'message':"Please login first, your session might have expired"}, 401
        except Exception as e:
            raise e
            return {'message': 'An error occured while decoding token.', 'error':str(e)},400
    return decorated

def is_blank(var):
    '''checks if any required field is blank''' 
    if var.strip() == '':
        return 'All fields are required'
    return None 