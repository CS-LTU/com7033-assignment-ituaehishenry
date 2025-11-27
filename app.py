from flask import Flask, render_template, request, redirect, url_for, flash

# To automate the webbrowser the webbrowser is imported below.
import webbrowser
#Threading allows multple running of tasks at the same time.
from threading import Thread
import time
import sqlite3
import os
""" For stronger security of password_hashing -
# using bcrypt implace of the built in security in flask - Werkzeug.
"""
import bcrypt


app = Flask(__name__)
# introducing cookies for security
app.secret_key = 'your-secret-key-here'

#Setting SQLite for authentication of user
def init_db():
    
    # Initialising the SQLite DB for user data
    conn = sqlite3.connect('users2.db')
    cursor =conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     first_name Text NOT NULL,
                     last_name  TEXT NOT NULL,
                     username Text UNIQUE,
                     password Text,
                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                     )
                   """ )
    conn.commit()
    conn.close()

        
 # Starting with route for the home page
@app.route('/')
def home():
    return render_template("index.html")

# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html")

# Route for the Help and Support page
@app.route('/help')
def Support():
    return render_template("help.html")

# routing for users registration
@app.route('/register', methods =['GET','POST'])
def let_register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']#.encode('utf-8')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        try: 
            conn = sqlite3.connect('users2.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (first_name, last_name, username, password) VALUES (?,?,?,?)",
                            (first_name, last_name, username, hashed_password))
            conn.commit()
            conn.close()
            return render_template("success.html")
            
        
        except Exception as e:
            flash(f"Error: {e}", "error")
            return redirect(url_for("let_register"))
    return render_template("Register.html")

#Routing for login
@app.route('/login', methods = ['GET', 'POST'])
def let_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users2.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username =?",(username,))
        record = cursor.fetchone()
        conn.close()

        if record and bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8')):
            flash("Login was successful!", "success")
            return redirect(url_for("home"))
        else:
            flash('Invalid username or password', "error")
            return redirect(url_for('let_login'))
    return render_template('Login.html')
          

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("Starting server...")
    Thread(target=run_flask).start()
    Thread(target=open_browser).start()