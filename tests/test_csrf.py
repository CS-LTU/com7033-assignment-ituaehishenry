import unittest
from flask import Flask, session, request
#csrf test

app = Flask(__name__)
app.secret_key = 'test'
app.testing = True

@app.route('/protect', methods=['POST'])
def protect():
    token = session.get('csrf_token')
    form_token = request.form.get('csrf_token')

    if not token or token != form_token:
        return 'CSRF Error', 400

class CSRFTests(unittest.TestCase):
    def test_csrf_protection(self):
        client = app.test_client()

        #attempt POST without CSRF token
        response = client.post('/protect')
        self.assertEqual(response.status_code, 400)   

if __name__ == '__main__':
    unittest.main()     