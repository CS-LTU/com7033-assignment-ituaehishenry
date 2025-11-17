from flask import Flask, render_template, request, redirect, url_for, flash

# To automate the webbrowser the webbrowser is imported below.
import webbrowser
#Threading allows multple running of tasks at the same time.
from threading import Thread
import time

app = Flask(__name__)
 # Starting with route for the home page
@app.route('/')
def home():
    return render_template("index.html")

# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# Route for the about page
@app.route('/help')
def Support():
    return render_template("help.html")



def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("Starting server...")
    Thread(target=run_flask).start()
    Thread(target=open_browser).start()