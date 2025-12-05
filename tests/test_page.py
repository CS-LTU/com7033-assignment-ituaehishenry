import unittest
from flask import Flask

# Create test app - I tried importing app from app but it was not recognising it- 
# saying no name module app. 
# spent time trying to figure it out  but no solution so I have to employ this method
app = Flask(__name__)

@app.route('/')
def home():
    return 'Home'

@app.route('/about')
def about():
    return 'About'
@app.route('/help')
def Support():
    return 'Support'

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
    
    def test_home(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
    
    def test_about(self):
        r = self.client.get('/about')
        self.assertEqual(r.status_code, 200)

    def test_help(self):
        r = self.client.get('/help')
        self.assertEqual(r.status_code, 200)    

if __name__ == '__main__':
    unittest.main()


