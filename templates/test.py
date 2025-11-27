
from flask import Flask
import sqlite3

app = Flask(__name__)

print("Flask app starting...")
print("SQLite version:", sqlite3.sqlite_version)

# Simple database setup
def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, content TEXT)''')
    c.execute("INSERT INTO messages (content) VALUES ('Hello SQLite!')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return "Hello Flask with SQLite! Database is ready."

@app.route('/messages')
def show_messages():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages")
    messages = c.fetchall()
    conn.close()
    return f"Messages: {messages}"

if __name__ == '__main__':
    init_db()  # Initialize database when app starts
    app.run(debug=True)
2. 
