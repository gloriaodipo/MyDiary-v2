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

    @token_required
    def get(self, user_id, entry_id=None):
        if entry_id:
            user_entry = Entry.get(user_id=user_id, entry_id=entry_id)
            if user_entry:
                return {'message': 'Entry found', 'entry': Entry.entry_dict(user_entry)}, 200
            else:
                return {'message': 'Entry not found'}, 404
        user_entries = Entry.get(user_id=user_id)
        return {'message': 'Entries found', 'entries': [Entry.entry_dict(entry)
         for entry in user_entries]}, 200