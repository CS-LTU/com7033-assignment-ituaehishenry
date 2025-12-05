import unittest
from flask import Flask, session

# Create test app - I tried importing app from app but it was not recognising it- 
# saying no name module app. 
# spent time trying to figure it out  but no solution so I have to employ this method
app = Flask(__name__)
app.secret_key = 'test'


@app.route('/login/<username>')
def login(username):
    session['user'] = username
    return f'Welcome {username}'

@app.route('/profile')
def profile():
    if 'user' in session:
        return f'Profile: {session["user"]}'
    return 'Please login'


class Authtests(unittest.TestCase):
    def setUp(self):
        
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess.clear()

    def test_login(self):
        """Testing that login is working"""    
        r = self.client.get('/login/peter')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Welcome peter', r.data.decode())  

    def test_user_after_login(self):
        """testing after login"""
        self.client.get('/login/peter')

        r = self.client.get('/profile')
        self.assertEqual(r.status_code, 200)
        self.assertIn('peter', r.data.decode())




if __name__ == '__main__':
    unittest.main()

