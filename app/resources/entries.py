from flask import Flask, request
from flask_restful import Resource, reqparse

from app.models import Entry
from app.decorators import token_required, is_blank

class EntryResource(Resource):
    '''Resource for diary entries'''
    parser = reqparse.RequestParser()
    parser.add_argument('title', required = True, type=str, help='Title cannot be blank')
    parser.add_argument('description', required = True, type=str, help='Description cannot be blank')

    @token_required
    def post(self, user_id):
        '''Method for adding an entry'''
        args = EntryResource.parser.parse_args()
        title = args.get('title', '')
        description = args.get('description', '')

        if is_blank(title) or is_blank(description):
            return {'message': 'All fields are required'}, 400
        entry =  Entry(title=title, user_id=user_id, description=description)
        entry.add()
        entries = Entry.get(user_id=user_id)
        return {'message': 'Entry has been published', 
        'entry': [Entry.entry_dict(entry) for entry in entries]}, 201
