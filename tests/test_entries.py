import json

from .base import BaseTestClass

ADD_ENTRY_URL = '/api/v1/user/entries'
GET_SINGLE_URL = '/api/v1/user/entries/1'
GET_ALL_URL = '/api/v1/user/entries'
DELETE_URL = '/api/v1/user/entries/1'
MODIFY_URL = '/api/v1/user/entries/1'

class Test_Entry_Case(BaseTestClass):
    '''Class for entry test cases'''
    def test_add_entry(self):
        '''Test API can add entry made by logged in user'''
        response = self.logged_in_user()

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "Entry has been published")

    def test_get_single_entry(self):
        '''Test API can get a single diary entry'''
        response = self.logged_in_user()

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get (GET_SINGLE_URL,
            content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["message"], "Entry found")

    def test_get_all_entries(self):
        '''Test API can get all diary entries'''
        response = self.logged_in_user()

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.get(GET_ALL_URL,
            content_type = 'application/json')
        entries = self.entry_model.get(user_id=1)
        entries = [self.entry_model.entry_dict(entry) for entry in entries]
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['entries'], entries)
        self.assertEqual(result["message"], "Entries found")
    
    def test_delete_entry(self):
        '''Test API can delete a diary entry'''
        response = self.logged_in_user()

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.delete(DELETE_URL,
        data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_modify_entry(self):
        '''Test API can modify a diary entry'''
        response = self.logged_in_user()

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)

        response = self.client.put(MODIFY_URL,
            data = json.dumps(dict(title="Modified title")),content_type = ("application/json"))
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual('Entry updated successfully', result['message'])
        self.assertEqual('Modified title', result['new_entry']['title']) 

    def test_cannot_add_entry_without_login(self):
        '''Test API cannot add entry if user is not logged in'''

        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertEqual(result["message"], "Please login first, your session might have expired")
        
    def test_cannot_get_single_entry_without_login(self):
        '''Test API cannot get a single diary entry without login'''
        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')

        response = self.client.get (GET_SINGLE_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Please login first, your session might have expired")

    def test_cannot_get_all_entries_without_login(self):
        '''Test API cannot get all diary entries without login'''
        response = self.client.post(ADD_ENTRY_URL,
            data = json.dumps(self.entry_data), content_type = 'application/json')

        response = self.client.get(GET_ALL_URL,
        data = json.dumps(self.entry_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 401)
