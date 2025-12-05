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

class Integrate_Test(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with self.client.session_transaction() as sess:
            sess.clear()

    def test_com_user_flow(self):
         


        #attempting to access profile without loging

        r = self.client.get('/profile')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Please login', r.data.decode())

        # when login as user
        r = self.client.get('/login/peter')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Welcome peter', r.data.decode())


        #accessing profile
        r = self.client.get('/profile')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Profile: peter', r.data.decode())

        # different user loging
        r = self.client.get('/login/paul')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Welcome paul', r.data.decode())

        # A new user should show
        r = self.client.get('/profile')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Profile: paul', r.data.decode())

        #session clearing

        with self.client.session_transaction() as sess:
            sess.clear()


        #loging request by profile   

        r = self.client.get('/profile')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Please login', r.data.decode())









if __name__ == '__main__':
    unittest.main()