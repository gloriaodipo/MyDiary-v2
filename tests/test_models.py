from .base import BaseTestClass

class TestModels(BaseTestClass):
    '''Class for models test cases'''

    def test_can_create_user(self):
        '''Test successful user creation'''
        self.user1.add()
        u = self.user_model.get('users', username=self.user1.username)
        self.assertEqual(u[1], self.user1.username)
        
    def test_can_create_entry(self):
        '''Test successful entry creation'''
        self.user1.add()
        self.entry1.add()
        entry = self.entry_model.get(user_id=1, entry_id=1)
        entry = self.entry_model.entry_dict(entry)
        self.assertEqual(entry['description'], self.entry1.description)
        self.assertEqual(entry['title'], self.entry1.title)
        
    def test_can_delete_user(self):
        '''Test successful deletion of user'''
        self.user1.add()
        user = self.user_model.get('users',id=1)
        self.user_model.delete('users', id=1)
        user = self.user_model.get('users',id=1)
        self.assertIsNone(user)
    
    def test_can_update_user_details(self):
        '''Test successful update of user'''
        self.user1.add()
        user = self.user_model.get('users', id=1)
        self.user_model.update('users', 1, data={'username':'New'})
        user = self.user_model.get('users', id=1)
        self.assertEqual(user[1], 'New')

    def test_get_non_existent_user(self):
        '''Test model cannot get a non-existent user'''
        user = self.user_model.get('users', id=3)
        self.assertIsNone(user)
    
    def test_get_user(self):
        '''Test can successfully get a user'''
        self.user1.add()
        user = self.user_model.get('users', id=1)
        user = self.user_model.user_dict(user)

        self.assertIsInstance(user, dict)
        keys = sorted(list(user.keys()))
        self.assertListEqual(keys, sorted(['username', 'email', 'id']))
    
    def test_can_validate_password(self):
        '''Test successful validation of password'''
        self.user1.add()
        self.assertTrue(
            self.user_model.validate_password(
                username=self.user1.username, password='password'))
        self.assertFalse(
            self.user_model.validate_password(
                username=self.user1.username, password='passw'))
    
    def test_can_update_entry(self):
        '''Test successful update of entries'''
        self.user1.add()
        self.entry1.add()
        entry = self.entry_model.get(user_id=1, entry_id=1)
        self.entry_model.update('entries', id=1, data={'title': 'New'})
        entry = self.entry_model.get(entry_id=1, user_id=1)
        entry = self.entry_model.entry_dict(entry)
        self.assertEqual(entry['title'], 'New')
    
    def test_can_get_one_entry(self):
        '''Test can successfully fetch one entry'''
        self.user1.add()
        self.entry1.add()
        entry = self.entry_model.get(user_id=1, entry_id=1)
        entry = self.entry_model.entry_dict(entry)
        self.assertIsInstance(entry, dict)
        keys = sorted(list(entry.keys()))
        self.assertListEqual(
            keys, sorted(['title', 'description', 'user_id', 
            'last_modified', 'created_at', 'id']))
    
    def test_can_get_all_entries(self):
        '''Test can successfully fetch all entries'''
        self.user1.add()
        self.entry1.add()
        entry = self.entry_model.get(user_id=1)
        self.assertEqual(1, len(entry))
        entry = self.entry_model.entry_dict(entry[0])
        self.assertIsInstance(entry, dict)

    def test_can_delete_an_entry(self):
        '''Test successful deletion of an entry'''
        self.user1.add()
        self.entry1.add()
        self.entry_model.delete(table='entries', id=1)
        entry = self.entry_model.get(user_id=1, entry_id=1)
        self.assertIsNone(entry)

    def test_cannot_get_non_existent_entry(self):
        '''Test model cannot get non-existent entry'''
        self.user1.add()
        entry = self.entry_model.get(entry_id=2, user_id=1)
        self.assertIsNone(entry)