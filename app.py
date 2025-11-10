from flask import Flask
import webbrowser
from threading import Thread
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Henry. This is a flask library"

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("Starting server...")
    Thread(target=run_flask).start()
    Thread(target=open_browser).start()