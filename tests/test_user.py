import json

from .base import BaseTestClass, SIGNUP_URL, LOGIN_URL

class Test_User_Case(BaseTestClass):
    '''User test cases'''    

    def test_signup(self):
        """Test API can successfully register a new user (POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps(self.user_data), content_type = 'application/json')
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Successfully registered")

    def test_wrong_signup(self):
        """Test API cannot successfully register a new user if any field is left blank(POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps({'username': 'gloria', 'email':'godipo@gmail.com', 'password':''}) ,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "All fields are required")
        
    def test_cannot_signup_twice(self):
        """Test API cannot register a user twice(POST request)"""
        self.client.post(SIGNUP_URL,
            data = json.dumps(self.user_data), content_type = 'application/json')
        response2 = self.client.post(SIGNUP_URL, 
            data = json.dumps(self.user_data), content_type = 'application/json')
        self.assertEqual(response2.status_code, 203)
        result = json.loads(response2.data.decode())
        self.assertEqual(result["message"], "That username or email is taken.")
        
    def test_cannot_signup_with_invalid_username(self):
        """Test API cannot successfully register user if username invalid(POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps({'username': '#$gloria', 'email':'godipo@gmail.com', 'password':'passw'}) ,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid username")

    def test_cannot_signup_with_wrong_email_format(self):
        """Test API cannot successfully register user if email is invalid(POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps({'username': 'gloria', 'email':'godipogmail.com', 'password':'passw'}) ,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Invalid email. Ensure email is of the form example@mail.com")
        
    def test_cannot_signup_with_short_username(self):
        """Test API cannot successfully register user if username is less than 4 char.(POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps({'username': 'glo', 'email':'godipo@gmail.com', 'password':'password'}) ,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Username should be atleast 4 characters")

    def test_cannot_signup_with_short_password(self):
        """Test API cannot successfully register user if password is less than 8 char.(POST request)"""
        response = self.client.post(SIGNUP_URL,
            data = json.dumps({'username': 'gloriao', 'email':'godipo@gmail.com', 'password':'pass'}) ,
            content_type = 'application/json')
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Password should be atleast 8 characters")

    def test_login(self):
        """Test API can successfully log in registered users using username and password (POST request)"""
        self.test_user.add()
        response = self.client.post(LOGIN_URL,
            data=json.dumps({'username': 'gloria', 'password': 'password'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You are successfully logged in")
        
    def test_wrong_password(self):
        """Test API cannot authenticate login when wrong password is used (POST request)"""
        self.test_user.add()
        response = self.client.post(LOGIN_URL,
            data=json.dumps({'username': 'gloria', 'password': 'wrong_password'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Username or password is wrong.')
        
    def test_login_nonexistent_user(self):
        """Test API cannot authenticate login when user is nonexistent (POST request)"""
        response = self.client.post(LOGIN_URL,
            data=json.dumps({'username': 'nonexistent', 'password': 'wrong_password'}),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User unavailable')